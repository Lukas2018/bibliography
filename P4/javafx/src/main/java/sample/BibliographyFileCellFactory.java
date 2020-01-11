package sample;

import javafx.scene.control.ListCell;
import javafx.scene.control.ListView;
import javafx.util.Callback;

public class BibliographyFileCellFactory implements Callback<ListView<BibliographyFile>, ListCell<BibliographyFile>>
{
    @Override
    public ListCell<BibliographyFile> call(ListView<BibliographyFile> listView)
    {
        return new BibliographyFileCell();
    }
}
