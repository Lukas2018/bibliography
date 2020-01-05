package sample;

public class File {
    private int id;
    private String fileName;

    public File(int id, String fileName) {
        this.id = id;
        this.fileName = fileName;
    }

    public int getId() {
        return id;
    }

    public String getFileName() {
        return fileName;
    }
}
