/**
 * 
 * 
 *  SCRIPTS TEMPORÁRIOS APENAS PARA DESENVOLVIMENTO DAS TELAS E VISUALIZAÇÃO DOS MODAIS E ALERTS
 * 
 * 
 * 
 */

$(document).ready(function () {
    // Evento de clique no botão
    $('#btSubmit').on('click', function (event) {
      event.preventDefault(); // Impede o envio do formulário
      var password = $('#password_field').val();

      // Verifica se o comprimento da senha é menor que 3
      if (password.length < 3) {
        $('#alert').show(); // Mostra o alerta
      } else {
        $('#alert').hide(); // Esconde o alerta se a senha for válida
      }
    });

    // Evento de clique em qualquer parte da tela
    $(document).on('click', function (event) {
      // Verifica se o clique não foi dentro do alerta ou do formulário
      if (!$(event.target).closest('#alert, .signin-form').length) {
        $('#alert').hide(); // Esconde o alerta
      }
    });

    // Evento de clique no botão de cadastro
    $('#btRegister').on('click', function(event) {
          event.preventDefault(); // Impede o envio do formulário de cadastro

          var email = $('#email_field').val();
          var password = $('#password_field').val();
          var confirmPassword = $('#confirm_password_field').val();
          var username = $('#username_field').val();

          // Reset alerts
          $('#alert-email').hide();
          $('#alert-password-mismatch').hide();
          $('#alert-password-policy').hide();
          $('#alert-success').hide();

          // Verifica se todos os campos estão preenchidos
          if (!email || !username || !password || !confirmPassword) {
              $('#alert-email').show(); // Mostra o alerta de campos vazios
              $('#alert-password-mismatch').show(); // Mostra o alerta de campos vazios
              $('#alert-password-policy').show(); // Mostra o alerta de campos vazios
          } else if (email === 'teste@example.com' || username === 'testuser') {
              $('#alert-email').show(); // Mostra o alerta de email/usuário já cadastrado
          } else if (password !== confirmPassword) {
              $('#alert-password-mismatch').show(); // Mostra o alerta de senhas não compatíveis
          } else if (!/^(?=.*[a-zA-Z])(?=.*\d)[a-zA-Z\d]{8,}$/.test(password)) {
              $('#alert-password-policy').show(); // Mostra o alerta de política de senha
          } else {
              $('#alert-success').show(); // Mostra o alerta de sucesso
              setTimeout(function() {
                  // Redireciona para a tela de login após 2 segundos
                  $('#registrationModal').modal('hide');
              }, 2000);
          }
      });

      // Evento de clique em qualquer parte da tela para esconder alertas
      $(document).on('click', function(event) {
          // Verifica se o clique não foi dentro dos alertas ou do formulário
          if (!$(event.target).closest('#alert-email, #alert-password-mismatch, #alert-password-policy, #alert-success, #registrationForm, #loginForm').length) {
              $('#alert-email').hide(); // Esconde o alerta
              $('#alert-password-mismatch').hide(); // Esconde o alerta
              $('#alert-password-policy').hide(); // Esconde o alerta
              $('#alert-success').hide(); // Esconde o alerta
          }
      });
  });