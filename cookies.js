const express = require('express');
const session = require('express-session');
const csrf = require('csurf');
const helmet = require('helmet');
const cookieParser = require('cookie-parser');

const app = express();

// Configurações de cabeçalhos de segurança com Helmet
app.use(helmet());

// Configuração de cookie seguro para sessões
app.use(session({
    name: 'session_id',
    secret: 'chave-secreta',
    resave: false,
    saveUninitialized: false,
    cookie: {
        httpOnly: true, // Impede acesso via JavaScript
        secure: process.env.NODE_ENV === 'production', // Ativo apenas em HTTPS
        sameSite: 'Strict', // Restringe envio cross-site
        maxAge: 1000 * 60 * 60 // 1 hora
    }
}));

// Proteção CSRF
app.use(cookieParser());
app.use(csrf({ cookie: true }));

// Rota de exemplo com validação CSRF
app.post('/form', (req, res) => {
    // Processamento do formulário
    res.send('Formulário recebido com proteção CSRF');
});

app.listen(3000, () => {
    console.log('Servidor rodando na porta 3000');
});
