package sample;

import javafx.scene.control.ListCell;

public class BibliographyFileCell extends ListCell<BibliographyFile> {
    @Override
    public void updateItem(BibliographyFile bibliographyFileItem, boolean empty) {
        super.updateItem(bibliographyFileItem, empty);
        String fileName = null;
        if (bibliographyFileItem != null && !empty)
        {
            fileName = bibliographyFileItem.getFileName();
        }
        this.setText(fileName);
        setGraphic(null);
    }
}
