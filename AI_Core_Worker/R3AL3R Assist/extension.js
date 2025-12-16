const vscode = require('vscode');
const { Client } = require('pg');

const client = new Client({
  connectionString: "postgresql://postgres:password123@localhost:5432/r3aler_ai"  // CHANGE THIS
});
client.connect();

async function queryR3AL3R(prompt) {
  const res = await client.query(`
    SELECT topic, content FROM crypto_unit.knowledge 
    WHERE to_tsvector('english', topic || ' ' || content) @@ plainto_tsquery($1)
    UNION ALL
    SELECT topic, content FROM physics_unit.knowledge 
    WHERE to_tsvector('english', topic || ' ' || content) @@ plainto_tsquery($1)
    ORDER BY ts_rank_cd(to_tsvector(topic || ' ' || content), plainto_tsquery($1)) DESC
    LIMIT 3
  `, [prompt]);

  if (res.rows.length === 0) return `R3ÆLƎR: I am hungry for "${prompt}". Feed me more.`;

  return res.rows.map(r => `### ${r.topic}\n${r.content}`).join('\n\n');
}

function activate(context) {
  // Register as REAL AI MODEL
  const model = vscode.lm.registerLanguageModel({
    id: 'r3al3r',
    provideCompletionItems: async (document, position, context, token) => {
      const line = document.lineAt(position).text.substring(0, position.character);
      const response = await queryR3AL3R(line.trim());
      return [new vscode.InlineCompletionItem(response + "\n")];
    },
    provideChatResponse: async (messages, options, token) => {
      const last = messages[messages.length - 1].content;
      const answer = await queryR3AL3R(last);
      return [{ content: answer }];
    }
  });

  // Chat participant automatically uses the model now
  const participant = vscode.chat.createChatParticipant('chat.r3al3r', async (request, context, response) => {
    response.progress("R3ÆLƎR awakens...");
    const answer = await queryR3AL3R(request.prompt);
    response.markdown(answer);
  });
  participant.iconPath = vscode.Uri.joinPath(context.extensionUri, 'icon.png');

  context.subscriptions.push(model, participant);
}

function deactivate() {
  client.end();
}

module.exports = { activate, deactivate };