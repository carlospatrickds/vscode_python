<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <title>Calculadora Simples</title>
  <style>
    body { font-family: Arial, sans-serif; max-width: 400px; margin: 40px auto; }
    input { width: 80px; margin: 5px; }
    button { width: 40px; margin: 5px; }
    #resultado { margin-top: 20px; font-size: 1.2em; }
  </style>
</head>
<body>
  <h2>Calculadora Simples</h2>
  <input id="campo1" type="number" placeholder="Campo 1">
  <input id="campo2" type="number" placeholder="Campo 2">
  <br>
  <button onclick="calcular('+')">+</button>
  <button onclick="calcular('-')">-</button>
  <button onclick="calcular('*')">*</button>
  <button onclick="calcular('/')">/</button>
  <div id="resultado"></div>

  <script>
    function calcular(operacao) {
      const campo1 = parseFloat(document.getElementById('campo1').value);
      const campo2 = parseFloat(document.getElementById('campo2').value);
      let resultado = '';
      if(isNaN(campo1) || isNaN(campo2)) {
        resultado = 'Por favor, preencha os dois campos.';
      } else {
        switch(operacao) {
          case '+': resultado = campo1 + campo2; break;
          case '-': resultado = campo1 - campo2; break;
          case '*': resultado = campo1 * campo2; break;
          case '/': 
            resultado = campo2 !== 0 ? (campo1 / campo2) : 'Divisão por zero!'; 
            break;
          default: resultado = 'Operação inválida.';
        }
      }
      document.getElementById('resultado').innerText = 'Resultado: ' + resultado;
    }
  </script>
</body>
</html>
