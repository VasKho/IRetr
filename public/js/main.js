const body_load = () => {
  const search_field = document.querySelector(".search-input");
  search_field.onkeypress = (e) => {
    if (!e) e = window.event;
    var keyCode = e.code || e.key;
    if (keyCode == 'Enter') {
      search(search_field.value);
    }
  };

  document.querySelector("#help").onclick = () => {
    const text = 'To start search just type your query in the search bar and press "Enter"\n To specify the word that must be in the document wrap it with double quotes ("")';
    create_popup(text);
  };

  document.querySelector("#metrics").onclick = () => {
    let text = '',
	recall = "recall: 0.75391\n",
	precision = "precision: 0.76815\n",
	accuracy = "accuracy: 0.83012\n",
	error = "error: 0.29147\n",
	f_measure = "f-measure: 0.73934\n";
    text += recall + precision + accuracy + error + f_measure;
    create_popup(text);
  };
};

const open_url = (url) => {
  window.open(url, '_blank').focus();
};

const search = async (query) => {
  if (query === "") return;
  const response = await fetch("/search", {
    method: "POST",
    mode: "same-origin",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ "query": query })
  }).then(response=>response.json());
  
  document.querySelector('.search-results').replaceChildren();
  for (const doc of response["results"]) {
    add_search_result(doc.name, doc.words, doc.url);
  }
  for (const doc of response["recommendations"]) {
    add_search_result(`${doc.name} [RECOMMENDED]`, doc.words, doc.url);
  }
};

const add_search_result = (name, words, url) => {
  const search_results = document.querySelector('.search-results');
  let wrapper = document.createElement('div');
  wrapper.className = "query-result-wrapper";
  let doc_name = document.createElement("div");
  doc_name.className = "result-document-name";
  doc_name.innerHTML = name;
  doc_name.onclick = () => { open_file(url); };
  let doc_words = document.createElement("div");
  doc_words.className = "result-document-words";
  doc_words.innerHTML = words;
  wrapper.appendChild(doc_name);
  wrapper.appendChild(doc_words);
  search_results.appendChild(wrapper);
};

const open_file = async (url) => {
  const response = await fetch(url, {
    mode: "same-origin",
    headers: { "Content-Type": "text/plain" }
  }).then(response=>response.blob());
  create_popup(await response.text());
};

const create_popup = async (content) => {
  const popup_box = document.createElement("div");
  popup_box.className = "popup";
  const close_button = document.createElement("button");
  close_button.className = "close-button";
  close_button.textContent = "close";
  close_button.onclick = () => {
    popup_box.parentNode.removeChild(popup_box);
  };
  popup_box.appendChild(close_button);
  const text_box = document.createElement("div");
  text_box.innerText = content;
  popup_box.appendChild(text_box);
  document.body.appendChild(popup_box);
};
