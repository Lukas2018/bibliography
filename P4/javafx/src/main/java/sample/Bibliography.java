package sample;

import java.time.LocalDate;
import java.util.Date;

public class Bibliography {
    private int id;
    private String name;
    private String author;
    private Date date;
    private String owner;
    private Date publication_date;

    public Bibliography(int id, String name, String author, Date date, String owner, Date publication_date) {
        this.id = id;
        this.name = name;
        this.author = author;
        this.date = date;
        this.owner = owner;

        this.publication_date = publication_date;
    }

    public int getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public String getAuthor() {
        return author;
    }

    public Date getDate() {
        return date;
    }

    public String getOwner() {
        return owner;
    }

    public Date getPublication_date() {
        return publication_date;
    }
}
