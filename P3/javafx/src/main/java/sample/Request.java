package sample;

import org.json.JSONObject;
import org.omg.CORBA.NameValuePair;

import java.io.*;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLEncoder;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;

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
            wr.close();
        }
        StringBuilder sb = new StringBuilder();
        OutputStream out = new FileOutputStream("out.pdf");
        int HttpResult = connection.getResponseCode();
        if (HttpResult == HttpURLConnection.HTTP_OK) {
            BufferedReader br = new BufferedReader(
                    new InputStreamReader(connection.getInputStream(), "utf-8"));
            String line;
            while ((line = br.readLine()) != null) {
                sb.append(line + "\n");
                out.write(line.getBytes());
            }
            br.close();
            out.close();
            System.out.println("" + sb.toString());
        } else {
            System.out.println(connection.getResponseMessage());
        }
        return sb.toString();
    }

    private byte[] getFileByRequest(String target, String requestType, JSONObject json) throws IOException {
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
            wr.close();
        }
        int HttpResult = connection.getResponseCode();
        byte[] file = null;
        if (HttpResult == HttpURLConnection.HTTP_OK) {
            InputStream in = connection.getInputStream();
            ByteArrayOutputStream out = new ByteArrayOutputStream();
            byte[] buf = new byte[131072];
            int n;
            while (-1!=(n=in.read(buf)))
            {
                out.write(buf, 0, n);
            }
            out.close();
            in.close();
            file = out.toByteArray();
            return file;
        } else {
            System.out.println(connection.getResponseMessage());
        }
        return file;

    }

    public String getListOfBibliographies() throws IOException {
        String target = targetURL + username;
        return sendRequest(target, "GET", null);
    }

    public void createBibliography(String bibliographyName, String bibliographyAuthor, String bibliographyDate, String token) throws IOException {
        String target = targetURL + username + "/bibliography";
        JSONObject json = new JSONObject();
        json.put("name", bibliographyName);
        json.put("author", bibliographyAuthor);
        json.put("date", bibliographyDate);
        json.put("token", token);
        sendRequest(target, "POST", json);
    }

    public void editBibliography(int bibliographyId, String bibliographyName, String bibliographyAuthor, String bibliographyDate, String token) throws IOException {
        String target = targetURL + username + "/bibliography/" + bibliographyId;
        JSONObject json = new JSONObject();
        json.put("name", bibliographyName);
        json.put("author", bibliographyAuthor);
        json.put("date", bibliographyDate);
        json.put("token", token);
        sendRequest(target, "POST", json);
    }

    public void deleteBibliography(String bibliographyId, String token) throws IOException {
        String target = targetURL + username + "/bibliography/" + bibliographyId;
        JSONObject json = new JSONObject();
        json.put("token", token);
        sendRequest(target, "DELETE", json);
    }

    public String getListOfFiles(int bibliographyId) throws IOException {
        String target = targetURL + username + "/bibliography/" + bibliographyId + "/details";
        return sendRequest(target, "GET", null);
    }

    public byte[] downloadFile(int fileId, String token) throws IOException {
        String target = targetURL + username + "/bibliography/file/" + fileId + "/download";
        JSONObject json = new JSONObject();
        json.put("token", token);
        return getFileByRequest(target, "POST", json);
    }

    public void deleteFile(int fileId, String token) throws IOException {
        String target = targetURL + username + "/bibliography/file/" + fileId + "/delete";
        JSONObject json = new JSONObject();
        json.put("token", token);
        sendRequest(target, "DELETE", json);
    }
}
