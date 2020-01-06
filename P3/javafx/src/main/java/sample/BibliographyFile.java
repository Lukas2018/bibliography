package sample;

public class BibliographyFile {
    private int id;
    private String fileName;

    public BibliographyFile(int id, String fileName) {
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
