// Abe Gomez
// trix-custom.js
// <abraham.gomez@student.cune.edu>
//
// This file was created to help with the persistent issue of certain
// trix toolbar buttons not wanting to live update as posts were being
// made. They would only show when published. Because of this, certain
// buttons were deleted so that new ones could be implemented with
// live update features.

function initializeCustomToolbarButtons(toolbarElement) {

    // Remove the original heading buttons
    const originalHeadingButton = toolbarElement.querySelector('[data-trix-attribute="heading1"]');
    if (originalHeadingButton) {
        originalHeadingButton.remove();
    }

    // Add custom button for Tt (downsize)
    if (!toolbarElement.querySelector('[data-trix-attribute="tt"]')) {
        const ttButtonHTML = '<button type="button" class="trix-button" data-trix-attribute="tt" title="Monospace" tabindex="-1" style="font-size: 1em">Tt</button>';
        toolbarElement.querySelector(".trix-button-group--block-tools").insertAdjacentHTML("afterbegin", ttButtonHTML);
    }

    // Add custom button for TT (upsize)
    if (!toolbarElement.querySelector('[data-trix-attribute="ttu"]')) {
        const ttUButtonHTML = '<button type="button" class="trix-button" data-trix-attribute="ttu" title="Monospace Upsize" tabindex="-1" style="font-size: 1em">TT</button>';
        toolbarElement.querySelector(".trix-button-group--block-tools").insertAdjacentHTML("afterbegin", ttUButtonHTML);
    }

    // Define Tt, TT, and attributes in Trix
    Trix.config.textAttributes.tt = { tagName: "span", style: { fontSize: "0.75em" }, inheritable: true };
    Trix.config.textAttributes.ttu = { tagName: "span", style: { fontSize: "1.5em" }, inheritable: true };

}

document.addEventListener("DOMContentLoaded", function() {
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            mutation.addedNodes.forEach(function(node) {
                if (node.nodeName === "TRIX-EDITOR") {
                    const toolbarElement = node.toolbarElement;
                    initializeCustomToolbarButtons(toolbarElement);
                }
            });
        });
    });

    observer.observe(document.body, { childList: true, subtree: true });

    // Apply custom toolbar buttons to existing Trix editors
    document.querySelectorAll("trix-editor").forEach(function(editor) {
        const toolbarElement = editor.toolbarElement;
        initializeCustomToolbarButtons(toolbarElement);
    });
});