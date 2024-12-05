const venom = require('venom-bot');
const qrcode = require('qrcode-terminal');
const axios = require('axios');
const { PDFDocument } = require('pdf-lib');
const fs = require('fs');
const path = require('path');

// Objeto para armazenar alunos validados
const alunosValidados = {};


// Inicializa o cliente do Venom Bot
venom.create({
    session: 'my-session',
    headless: false, // Mantenha o navegador visível para escanear o QR code
}).then((client) => {
    console.log('Cliente está pronto e conectado!');

    // Escaneia o QR code
    client.on('qr', (qr) => {
        qrcode.generate(qr, { small: true });
        console.log('QR code gerado, escaneie com o WhatsApp!');
    });

    // Escuta mensagens
    client.on('message', async (message) => {
        if (message.body === '/ajuda') {
            message.reply('Aqui estão os comandos disponíveis:\n /entrar como aluno - 1\n /entrar como adm - 2');
        }

        if (message.body === '1') {
            message.reply('Digite o RM e a senha neste formato: rm_aluno:senha_aluno');
        }

        if (message.body.includes(':')) {
            const [rm, senha] = message.body.split(':');
            const response = await axios.post('http://127.0.0.1:8000/alunos/validar', { rm, senha });
            
            if (response.data.validado) {
                const nome = response.data.nome;
                alunosValidados[message.from] = nome;
                message.reply(`Login como aluno bem-sucedido! Olá, ${nome}.\nComo posso ajudar?\n/AGENDAR - 5\n/CARDÁPIO - 6`);
            } else {
                message.reply('RM ou senha inválidos para aluno.');
            }
        }

        if (message.body === '5') {
            if (alunosValidados[message.from]) {
                const response_agenda = await axios.get('http://127.0.0.1:8000/alunos/agendar');
                if (response_agenda.data.agendado) {
                    const nome_agenda = response_agenda.data.nome;
                    message.reply(`AGENDAMENTO EFETUADO COM SUCESSO!\n\nNOME DO ALUNO:\n ${nome_agenda}`);
                }
            } else {
                message.reply('Você precisa estar logado como aluno para usar esse comando.');
            }
        }

        if (message.body === '!BANCOALUNOS') {
            const pdfPath = path.join(__dirname, 'ListaAlmoço.pdf');
            if (fs.existsSync(pdfPath)) {
                const media = await fs.promises.readFile(pdfPath);
                
                console.log('Tamanho do arquivo:', media.length);
                
                // Envia o PDF
                client.sendFile(
                    message.from, // Para quem enviar
                    compressedPath, // Caminho do arquivo comprimido
                    'ListaAlmoço_Comprimido.pdf', // Nome do arquivo
                    'Aqui está o PDF com os alunos!' // Legenda
                ).then(() => {
                    console.log('PDF enviado com sucesso!');
                }).catch((err) => {
                    console.error('Erro ao enviar PDF:', err);
                    message.reply('Ocorreu um erro ao enviar o PDF. Tente novamente mais tarde.');
                });
            } else {
                message.reply('O arquivo PDF não foi encontrado.');
            }
        }
    });
}).catch((error) => console.error('Erro ao criar cliente:', error));