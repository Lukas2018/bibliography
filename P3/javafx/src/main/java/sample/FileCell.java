package sample;

import javafx.scene.control.ListCell;

public class FileCell extends ListCell<File> {
    @Override
    public void updateItem(File fileItem, boolean empty) {
        super.updateItem(fileItem, empty);
        String fileName = null;
        if (fileItem != null && !empty)
        {
            fileName = fileItem.getFileName();
        }
        this.setText(fileName);
        setGraphic(null);
    }
}
