package sample.controllers;

import javafx.fxml.FXML;
import javafx.scene.control.DatePicker;
import javafx.scene.control.ListView;
import javafx.scene.control.TextField;
import javafx.scene.layout.VBox;
import org.json.JSONArray;
import org.json.JSONObject;
import sample.Bibliography;
import sample.BibliographyCellFactory;
import sample.Request;
import sample.Token;

import java.io.IOException;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.time.LocalDate;
import java.time.ZoneId;
import java.util.ArrayList;
import java.util.Date;

public class IndexController {
    private Request request;
    private Token token;
    private Bibliography selectedBibliography = null;
    @FXML
    private ListView listView;
    @FXML
    private VBox vBoxLogin;
    @FXML
    private VBox vBoxMenu;
    @FXML
    private VBox vBoxCreate;
    @FXML
    private VBox vBoxEdit;
    @FXML
    private VBox vBoxDetails;
    @FXML
    private TextField login;
    @FXML
    private TextField nameCreate;
    @FXML
    private TextField authorCreate;
    @FXML
    private DatePicker dateCreate;
    @FXML
    private TextField nameEdit;
    @FXML
    private TextField authorEdit;
    @FXML
    private DatePicker dateEdit;
    public IndexController() {
        request = new Request();
        token = new Token();
    }

    @FXML
    public void initialize() {
        vBoxMenu.setVisible(false);
        vBoxMenu.setManaged(false);
        vBoxCreate.setVisible(false);
        vBoxCreate.setManaged(false);
        vBoxEdit.setVisible(false);
        vBoxEdit.setManaged(false);
        vBoxDetails.setVisible(false);
        vBoxDetails.setManaged(false);
        vBoxLogin.setVisible(true);
        vBoxLogin.setManaged(true);
        listView.setOnMouseClicked(event -> {
            Bibliography clickedBibliography = (Bibliography) listView.getSelectionModel().getSelectedItem();
            if(clickedBibliography != selectedBibliography) {
                selectedBibliography = clickedBibliography;
            }
            showBibliographyDetails();
        });
    }

    @FXML
    public void showApp() {
        if(login.getText() != null && !login.getText().trim().isEmpty()) {
            request.setUsername(login.getText().trim());
            token.setUsername(login.getText().trim());
            vBoxLogin.setVisible(false);
            vBoxLogin.setManaged(false);
            listView.getItems().addAll(createBibliographyList());
            listView.setCellFactory(new BibliographyCellFactory());
            vBoxMenu.setVisible(true);
            vBoxMenu.setManaged(true);
        }
    }

    @FXML
    public void synchronize() {
        listView.getItems().clear();
        listView.getItems().addAll(createBibliographyList());
    }

    @FXML
    public void showCreateForm() {
        vBoxEdit.setManaged(false);
        vBoxEdit.setVisible(false);
        vBoxDetails.setVisible(false);
        vBoxDetails.setManaged(false);
        vBoxCreate.setVisible(true);
        vBoxCreate.setManaged(true);
    }

    @FXML
    public void submitCreate() {
        String name = nameCreate.getText();
        String author = authorCreate.getText();
        LocalDate localDate = dateCreate.getValue();
        if(name != null && author != null && localDate != null && !name.trim().isEmpty() && !author.isEmpty()) {
            try {
                Date date = Date.from(localDate.atStartOfDay(ZoneId.systemDefault()).toInstant());
                request.createBibliography(name.trim(), author.trim(), date, "");
                synchronize();
                vBoxCreate.setVisible(false);
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }

    @FXML
    public void showEditForm() {
        if(selectedBibliography != null) {
            vBoxCreate.setManaged(false);
            vBoxCreate.setVisible(false);
            vBoxDetails.setVisible(false);
            vBoxDetails.setManaged(false);
            nameEdit.setText(selectedBibliography.getName());
            authorEdit.setText(selectedBibliography.getAuthor());
            dateEdit.setValue(selectedBibliography.getDate().toInstant().atZone(ZoneId.systemDefault()).toLocalDate());
            vBoxEdit.setVisible(true);
            vBoxEdit.setManaged(true);
        }
    }

    @FXML
    public void submitEdit() {
        int id = selectedBibliography.getId();
        String name = nameEdit.getText();
        String author = authorEdit.getText();
        Date date = Date.from(dateEdit.getValue().atStartOfDay(ZoneId.systemDefault()).toInstant());
        if(name != null && author != null && date != null && !name.trim().isEmpty() && !author.isEmpty()) {
            try {
                request.editBibliography(id, name.trim(), author.trim(), date, "");
                synchronize();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }

    @FXML
    public void deleteBibliography() {
        if(selectedBibliography != null) {
            try {
                String deleteToken = token.createBibliographyDeleteToken();
                request.deleteBibliography(String.valueOf(selectedBibliography.getId()), deleteToken);
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }

    private void showBibliographyDetails() {
        vBoxCreate.setManaged(false);
        vBoxCreate.setVisible(false);
        vBoxEdit.setVisible(false);
        vBoxEdit.setManaged(false);
        // załadowanie danych
        vBoxDetails.setVisible(true);
        vBoxDetails.setManaged(true);
    }

    private ArrayList<Bibliography> createBibliographyList()
    {
        ArrayList<Bibliography> bibliographies = new ArrayList<>();

        String resp = null;
        try {
            resp = request.getListOfBibliographies();
        } catch (IOException e) {
            e.printStackTrace();
        }
        JSONArray jArray = new JSONArray(resp);
        for(int i=0; i < jArray.length(); i++){
            JSONObject jObject = jArray.getJSONObject(i);
            int id = jObject.getInt("id");
            String name = jObject.getString("name");
            String author = jObject.getString("author");
            Date date = null;
            try {
                date = new SimpleDateFormat("yyyy-MM-dd").parse(jObject.getString("date"));
            } catch (ParseException e) {
                e.printStackTrace();
            }
            String owner = jObject.getString("owner");
            Date publication_date = null;
            try {
                publication_date = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss").parse(jObject.getString("publication_date"));
            } catch (ParseException e) {
                e.printStackTrace();
            }
            Bibliography bibliography = new Bibliography(id, name, author, date, owner, publication_date);
            bibliographies.add(bibliography);
        }

        return bibliographies;
    }
}
