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
        httpOnly: true,
        secure: true,        // Necessário para SameSite=None
        sameSite: 'None'     // Configura o atributo SameSite
    }
}));

// Proteção CSRF
app.use(cookieParser());
app.use(csrf({ cookie: true }));

// Middleware para processar dados do corpo
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Rota de exemplo com validação CSRF
app.post('/form', (req, res) => {
    // Processamento do formulário
    res.send('Formulário recebido com proteção CSRF');
});

// Inicia o servidor
app.listen(3000, () => {
    console.log('Servidor rodando na porta 3000');
});
