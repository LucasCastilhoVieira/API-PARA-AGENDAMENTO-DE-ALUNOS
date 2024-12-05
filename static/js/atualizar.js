document.getElementById("updateForm").addEventListener("submit", function(event) {


    // Obtém os valores dos campos do formulário
    const rm = document.getElementById("rm").value;
    const codigoEtec = document.getElementById("codigo_etec").value;
    const estado = document.getElementById("estado").value;

    // Mostra a mensagem de sucesso com os dados fornecidos
    const resultDiv = document.getElementById("result");
    resultDiv.innerHTML = `<p>Atualização efetuada com sucesso!</p>
                           <p><strong>RM:</strong> ${rm}</p>
                           <p><strong>Código ETEC:</strong> ${codigoEtec}</p>
                           <p><strong>Estado de Almoço:</strong> ${estado}</p>`;
    resultDiv.style.color = "green";

    // Opcional: Envie o formulário com Ajax se necessário
    // Se quiser realmente enviar o formulário ao servidor após a mensagem, descomente o código abaixo
    // this.submit();
});