package sample;

import javafx.scene.control.ListCell;
import javafx.scene.control.ListView;
import javafx.util.Callback;

public class FileCellFactory implements Callback<ListView<File>, ListCell<File>>
{
    @Override
    public ListCell<File> call(ListView<File> listView)
    {
        return new FileCell();
    }
}
