const { Client } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const axios = require('axios');
const client = new Client();
const alunosValidados = {};
const select_cardapio = {};
const verificator_msg = {};
const path = require('path');



client.on('qr', (qr) => {
    qrcode.generate(qr, { small: true });
    console.log('QR code gerado, escaneie com o WhatsApp!');
});

client.on('ready', () => {
    console.log('Cliente está pronto e conectado!');
});

client.on('message', async message => {

  

    if (message.body === '1') {
        verificator_msg[message.from] = true;
        message.reply('*PARA ACESSAR SUA SESSÃO, DIGITE SEU RM E SENHA NA FORMATAÇÃO ABAIXO:*\n\nSeuRM : SuaSenha\n\n*RM:* CÓDIGO DO ALUNO DO NSA 📝\n\n*SENHA:* VALIDAÇÃO DE LOGIN ATRAVÉS DA SENHA DO ALUNO 🔑');
    }



    if (message.body.includes(':') && verificator_msg[message.from]) {
        const [rm, senha] = message.body.split(':').map(item => item.trim());
        

        const response = await axios.post('http://127.0.0.1:8000/alunos/validar', {
            rm: rm,
            senha: senha   // Certifique-se de que o objeto enviado tem a estrutura correta
            });

            if (response.data.validado == true) {
                const nome = response.data.nome
                let nomes = `${nome}`
                let NAME = nomes.toUpperCase()
                alunosValidados[message.from] = NAME;
                message.reply(`‼️ *SEJA BEM VINDO, ${NAME}*‼️\n\n*COMO POSSO AJUDAR?* 🤖\n\n📅 *AGENDAR* | 5\n\n🗓️ *CARDÁPIO* | 6\n\n🏠 *SAIR* | 4`);

            }
            else{
                message.reply('RM OU SENHA INVÁLIDOS PARA BUSCA')
            }
        }


        if (message.body === '5') {
            if (alunosValidados[message.from]) {
                const response_agenda = await axios.get('http://127.0.0.1:8000/alunos/agendar')
                if (response_agenda.data.agendado == true){
                    const nome_agenda = response_agenda.data.nome
                    nome_completo = `${nome_agenda}`.toUpperCase()
                    message.reply(`✅ *AGENDAMENTO EFETUADO COM SUCESSO* ‼️\n\n*ALUNO* | *${nome_completo}*\n\n*"COOK SYSTEM"* 👾`)
                }
                
            } else {
                message.reply('Você precisa estar logado como aluno para usar esse comando.');
            }
        }

        if (message.body === '6') {
            if (alunosValidados[message.from]) {
                message.reply(
                    `📌 *QUAL DIA VOCÊ DESEJA SELECIONAR O CARDÁPIO?* 📌\n\n` +
                    `📅 *HOJE* - Digite *10*\n` +
                    `📅 *AMANHÃ* - Digite *11*\n`
                );
                select_cardapio[message.from] = 6;
            } else {
                message.reply('VOCÊ PRECISA ESTAR LOGADO PARA USAR ESSE COMANDO!');
            }
        }


        if (message.body === '10') {
            if (select_cardapio[message.from] && alunosValidados[message.from]) {

                const hoje = new Date();
                const anoHoje = hoje.getFullYear();
                const mesHoje = String(hoje.getMonth() + 1).padStart(2, '0'); // Adiciona 1 porque os meses começam de 0
                const diaHoje = String(hoje.getDate()).padStart(2, '0');
                const dataHoje = `${anoHoje}-${mesHoje}-${diaHoje}`;
                const request_cardapio = await axios.post('http://127.0.0.1:8000/alunos/cardapio_access',{date: dataHoje})
          
                
                const { cardapio, request } = request_cardapio.data;
                if(request){
                     message.reply(`CARDÁPIO DE HOJE: ${cardapio}`)
                }
                else{
                    message.reply('⚠️ *SEM LANÇAMENTO DE CARDÁPIO* ⚠️')
                }

            } else {
                message.reply('VOCÊ PRECISA ACESSAR A ÁREA DE CARDÁPIO!');
            }
        }

        if (message.body === '11') {
            if (select_cardapio[message.from] && alunosValidados[message.from]) {
                const hoje = new Date();
                const amanha = new Date();
                amanha.setDate(hoje.getDate() + 1); 
                const anoAmanha = amanha.getFullYear();
                const mesAmanha = String(amanha.getMonth() + 1).padStart(2, '0');
                const diaAmanha = String(amanha.getDate()).padStart(2, '0');
                const dataAmanha = `${anoAmanha}-${mesAmanha}-${diaAmanha}`;
                const request_cardapio = await axios.post('http://127.0.0.1:8000/alunos/cardapio_access',{date: dataAmanha})



                const { cardapio, request } = request_cardapio.data;
                if(request){
                     message.reply(`📅 *CARDÁPIO DE AMANHÃ:* \n\n* *${cardapio}* 🍗`)
                }
                else{
                    message.reply('⚠️ *SEM LANÇAMENTO DE CARDÁPIO* ⚠️')
                }

            } else {
                message.reply('VOCÊ PRECISA ACESSAR A ÁREA DE CARDÁPIO!');
            }

        }
 
        if (!verificator_msg[message.from]) {
            if (message.body) {
                message.reply('*Olá!* Você está falando com o atendimento eletrônico da *COOK SYSTEM*, como posso ajudar?\n\n🎓 *Entrar como Aluno* | Digite 1');
            }
        } 

        if (alunosValidados[message.from] && message.body === '4') {
            delete verificator_msg[message.from];
            delete alunosValidados[message.from];
            delete select_cardapio[message.from];
            message.reply('*Sessão encerrada.*\n\n*Olá!* Você está falando com o atendimento eletrônico da *COOK SYSTEM*, como posso ajudar?\n\n🎓 *Entrar como Aluno* | Digite 1');

            return; 
        }
    

    }

    

); 


client.initialize();
