package sample;

import javafx.scene.control.ListCell;
import javafx.scene.control.ListView;
import javafx.util.Callback;

public class BibliographyCellFactory implements Callback<ListView<Bibliography>, ListCell<Bibliography>>
{
    @Override
    public ListCell<Bibliography> call(ListView<Bibliography> listView)
    {
        return new BibliographyCell();
    }
}
