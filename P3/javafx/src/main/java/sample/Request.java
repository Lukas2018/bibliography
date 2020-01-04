package sample;

import org.json.JSONObject;

import java.io.*;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.Date;

public class Request {
    private HttpURLConnection connection = null;
    private URL url = null;
    private String targetURL = "http://localhost:5001/";
    private String username;

    public void setUsername(String username) {
        this.username = username;
    }

    private String sendRequest(String target, String requestType, JSONObject json) throws IOException {
        url = new URL(target);
        connection = (HttpURLConnection) url.openConnection();
        connection.setRequestMethod(requestType);
        connection.setRequestProperty("Content-Type", "application/json");
        connection.setRequestProperty("Accept", "application/json");
        connection.setDoInput(true);
        connection.setDoOutput(true);
        if(json != null) {
            OutputStreamWriter wr = new OutputStreamWriter(connection.getOutputStream());
            wr.write(json.toString());
            wr.flush();
        }
        StringBuilder sb = new StringBuilder();
        int HttpResult = connection.getResponseCode();
        if (HttpResult == HttpURLConnection.HTTP_OK) {
            BufferedReader br = new BufferedReader(
                    new InputStreamReader(connection.getInputStream(), "utf-8"));
            String line;
            while ((line = br.readLine()) != null) {
                sb.append(line + "\n");
            }
            br.close();
            System.out.println("" + sb.toString());
        } else {
            System.out.println(connection.getResponseMessage());
        }
        return sb.toString();
    }

    public String getListOfBibliographies() throws IOException {
        String target = targetURL + username;
        return sendRequest(target, "GET", null);
    }

    public String createBibliography(String bibliographyName, String bibliographyAuthor, Date bibliographyDate) throws IOException {
        String target = targetURL + username + "/bibliography";
        JSONObject json = new JSONObject();
        json.put("name", bibliographyName);
        json.put("author", bibliographyAuthor);
        json.put("date", bibliographyDate.toString());
        return sendRequest(target, "POST", json);
    }

    public String editBibliography(int bibliographyId, String bibliographyName, String bibliographyAuthor, Date bibliographyDate) throws IOException {
        String target = targetURL + username + "/bibliography/" + bibliographyId;
        JSONObject json = new JSONObject();
        json.put("name", bibliographyName);
        json.put("author", bibliographyAuthor);
        json.put("date", bibliographyDate.toString());
        return sendRequest(target, "POST", json);
    }

    public String deleteBibliography(String bibliographyId) throws IOException {
        String target = targetURL + username + "/bibliography/" + bibliographyId;
        return sendRequest(target, "DELETE", null);
    }
}
