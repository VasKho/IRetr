const body_load = () => {
  const search_field = document.querySelector(".search-input");
  search_field.onkeypress = (e) => {
    if (!e) e = window.event;
    var keyCode = e.code || e.key;
    if (keyCode == 'Enter') {
      search(search_field.value);
    }
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
  for (const doc of response) {
    add_search_result(doc.name, doc.words, doc.url);
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
    mode: "same-origin"
  }).then(response=>response.blob());
};
