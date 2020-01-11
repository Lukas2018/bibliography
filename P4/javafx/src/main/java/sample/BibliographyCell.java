package sample;

import javafx.scene.control.ListCell;

public class BibliographyCell extends ListCell<Bibliography> {
    @Override
    public void updateItem(Bibliography item, boolean empty)
    {
        super.updateItem(item, empty);
        String name = null;

        if (item != null && !empty)
        {
            name = item.getName();
        }

        this.setText(name);
        setGraphic(null);
    }
}
