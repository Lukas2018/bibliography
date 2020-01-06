package sample;

import javafx.fxml.FXML;
import javafx.scene.control.DatePicker;
import javafx.scene.control.Label;
import javafx.scene.control.ListView;
import javafx.scene.control.TextField;
import javafx.scene.layout.VBox;
import javafx.stage.DirectoryChooser;
import org.apache.commons.io.FileUtils;
import org.json.JSONArray;
import org.json.JSONObject;


import java.io.*;
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
    private BibliographyFile selectedBibliographyFile = null;
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
    @FXML
    private Label nameDetails;
    @FXML
    private Label authorDetails;
    @FXML
    private Label dateDetails;
    @FXML
    private Label ownerDetails;
    @FXML
    private Label publicationDateDetails;
    @FXML
    private ListView fileListView;

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
        fileListView.setOnMouseClicked(event -> {
            BibliographyFile clickedBibliographyFile = (BibliographyFile) fileListView.getSelectionModel().getSelectedItem();
            if(clickedBibliographyFile != selectedBibliographyFile) {
                selectedBibliographyFile = clickedBibliographyFile;
            }
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

    @FXML
    public void showCreateForm() {
        vBoxEdit.setManaged(false);
        vBoxEdit.setVisible(false);
        vBoxDetails.setVisible(false);
        vBoxDetails.setManaged(false);
        nameCreate.setText("");
        authorCreate.setText("");
        dateCreate.setValue(null);
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
                String createToken = token.createBibliographyCreateToken();
                request.createBibliography(name.trim(), author.trim(), localDate.toString(), createToken);
                synchronize();
                vBoxCreate.setVisible(false);
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }

    @FXML
    public void showEditForm() {
        if((selectedBibliography != null) && (listView.getSelectionModel().getSelectedItem() != null)) {
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
        LocalDate localDate = dateEdit.getValue();
        if(name != null && author != null && localDate != null && !name.trim().isEmpty() && !author.isEmpty()) {
            try {
                String editToken = token.createBibliographyEditToken();
                request.editBibliography(id, name.trim(), author.trim(), localDate.toString(), editToken);
                synchronize();
                vBoxEdit.setVisible(false);
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }

    @FXML
    public void deleteBibliography() {
        if((selectedBibliography != null) && (listView.getSelectionModel().getSelectedItem() != null)) {
            try {
                String deleteToken = token.createBibliographyDeleteToken();
                request.deleteBibliography(String.valueOf(selectedBibliography.getId()), deleteToken);
                synchronize();
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
        nameDetails.setText("Nazwa: " + selectedBibliography.getName());
        authorDetails.setText("Autor: " + selectedBibliography.getAuthor());
        dateDetails.setText("Data wydania: " + selectedBibliography.getDate().toString());
        ownerDetails.setText("Właściciel: " + selectedBibliography.getOwner());
        publicationDateDetails.setText("Data publikacji: " + selectedBibliography.getPublication_date().toString());
        fileListView.getItems().clear();
        fileListView.getItems().addAll(createFileList());
        fileListView.setCellFactory(new BibliographyFileCellFactory());
        vBoxDetails.setVisible(true);
        vBoxDetails.setManaged(true);
    }

    @FXML
    public void synchronizeFiles() {
        fileListView.getItems().clear();
        fileListView.getItems().addAll(createFileList());
    }

    private ArrayList<BibliographyFile> createFileList()
    {
        ArrayList<BibliographyFile> bibliographyFiles = new ArrayList<>();

        String resp = null;
        try {
            resp = request.getListOfFiles(selectedBibliography.getId());
        } catch (IOException e) {
            e.printStackTrace();
        }
        JSONArray jArray = new JSONArray(resp);
        for(int i=0; i < jArray.length(); i++){
            JSONObject jObject = jArray.getJSONObject(i);
            int id = jObject.getInt("id");
            String fileName = jObject.getString("filename");
            BibliographyFile bibliographyFile = new BibliographyFile(id, fileName);
            bibliographyFiles.add(bibliographyFile);
        }

        return bibliographyFiles;
    }

    @FXML
    public void downloadFile() {
        if((selectedBibliographyFile != null) && (fileListView.getSelectionModel().getSelectedItem() != null)) {
            String downloadFileToken = token.createFileDownloadToken();
            try {
                DirectoryChooser directoryChooser = new DirectoryChooser();
                File selectedDirectory = directoryChooser.showDialog(Main.getPrimaryStage());

                if(selectedDirectory != null){
                    byte[] file = request.downloadFile(selectedBibliographyFile.getId(), downloadFileToken);
                    FileOutputStream fos = new FileOutputStream(selectedDirectory.getAbsolutePath() + "\\" + selectedBibliographyFile.getFileName());
                    fos.write(file);
                    fos.close();
                    System.out.println(selectedDirectory.getAbsolutePath() + "\\dupa.pdf");
                }
                synchronizeFiles();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }

    @FXML
    public void deleteFile() {
        if((selectedBibliographyFile != null) && (fileListView.getSelectionModel().getSelectedItem() != null)) {
            String deleteFileToken = token.createFileDeleteToken();
            try {
                request.deleteFile(selectedBibliographyFile.getId(), deleteFileToken);
                synchronizeFiles();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }
}
