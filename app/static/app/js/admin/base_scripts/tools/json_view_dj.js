'use strict';
import JsonViewer from './json-viewer-js/src/jsonViewer.js';


function getJsonData(parentSelector) {
    const jsonBlock = document.querySelector(parentSelector);
    // Спрятать блок с JSON данными:
    if (jsonBlock) {
        jsonBlock.querySelector('div.form-row').style.display = 'none';
        
        const jsonData = jsonBlock.querySelector('textarea').innerText.trim();
        return jsonData;
    }
}


function setJSONBlock(parentSelector) {
    const parentBlock = document.querySelector(parentSelector);
    if (!parentBlock) return;

    const jsonBlock = document.querySelector('#json-container-view');
    const jsonData = getJsonData(parentSelector);
    // console.log("\n\nJSON Data:", jsonData);
    
    if (parentBlock && jsonBlock) {
        // parentBlock.insertAdjacentElement('afterend', jsonBlock);
        parentBlock.appendChild(jsonBlock);
    }

    try {
        // Проверяем, что данные можно распарсить как JSON
        JSON.parse(jsonData);

        new JsonViewer({
            container: jsonBlock,
            data: jsonData,
            theme: 'dark',
            expand: false
        });
    } catch (e) {
        jsonBlock.innerHTML = 'No JSON Data';
    }
}


export function setJSONBlocks(parentSelectors) {
    parentSelectors.forEach(selector => setJSONBlock(selector));
}