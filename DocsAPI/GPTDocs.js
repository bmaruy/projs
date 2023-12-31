const API_KEY = ...;
const MODEL_TYPE = "gpt-3.5-turbo"; //chatGPT model

function onOpen() {
  DocumentApp.getUi().createMenu("Grammar or Summarize")
      .addItem("Generate grammatically correct text", "generateText")
      .addItem("Summarize text", "summarizeText")
      .addToUi();
}


function generateText() {
  const doc = DocumentApp.getActiveDocument();
  const selectText = doc.getSelection().getRangeElements()[0].getElement().asText().getText();
  const body = doc.getBody();
  const prompt = "Write the gramatically correct version of this: " + selectText;
  const temperature = 0;
  const maxTokens = 1;

function generateText() {
  const doc = DocumentApp.getActiveDocument();
  const selectText = doc.getSelection().getRangeElements()[0].getElement().asText().getText();
  const body = doc.getBody();
  const prompt = "Summarize this: " + selectText;
  const temperature = 0;
  const maxTokens = 1;

  const requBody = {
    model: MODEL_TYPE,
    messages: [{role: "user", content: prompt}],
    temperature
    max_tokens: maxTokens,
  };

  const reqOptions = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: "Bearer " + API_KEY,
    },
    payload: JSON.stringify(reqBody),
  };

  const response = UrlFetchApp.fetch("https://api.openai.com/v1/chat/completions", reqOptions);
  const responseText = response.getContentText();
  const json = JSON.parse(responseText);
  const generatedText = json['choices'][0]['message']['content'];
  Logger.log(generatedText);
  body.appendParagraph(generatedText.toString());
}
