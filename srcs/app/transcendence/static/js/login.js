$(document).ready(function () {
    $('#btSubmit').on('click', function (event) {
      event.preventDefault(); 
      var password = $('#password_field').val();

      password.length < 3 ? $('#alert').show() : $('#alert').hide(); 
    });

    $(document).on('click', function (event) {
      if (!$(event.target).closest('#alert, .signin-form').length) {
        $('#alert').hide(); 
      }
    });

    
    $('#btRegister').on('click', function(event) {
        event.preventDefault(); 

        var email = $('#email_field').val();
        var password = $('#password_field').val();
        var confirmPassword = $('#confirm_password_field').val();
        var username = $('#username_field').val();

        $('#alert-email').hide();
        $('#alert-password-mismatch').hide();
        $('#alert-password-policy').hide();
        $('#alert-success').hide();

        if (!email || !username || !password || !confirmPassword) {
            $('#alert-email').show();
            $('#alert-password-mismatch').show();
            $('#alert-password-policy').show();
        }
        else if (email === 'teste@example.com' || username === 'testuser') {
            $('#alert-email').show(); 
        }
        else if (password !== confirmPassword) {
            $('#alert-password-mismatch').show(); 
        }
        else if (!/^(?=.*[a-zA-Z])(?=.*\d)[a-zA-Z\d]{8,}$/.test(password)) {
            $('#alert-password-policy').show(); 
        }
        else {
            $('#alert-success').show();
            setTimeout(function() {
                $('#registrationModal').modal('hide');
            }, 2000);
        }
    });

    $(document).on('click', function(event) {
        if (!$(event.target).closest('#alert-email, #alert-password-mismatch, #alert-password-policy, #alert-success, #registrationForm, #loginForm').length) {
            $('#alert-email').hide(); 
            $('#alert-password-mismatch').hide(); 
            $('#alert-password-policy').hide(); 
            $('#alert-success').hide(); 
        }
    });



/****   ESQUECI MINHA SENHA     ****/

     $('#toggleForm').on('click', function() {
        $('#emailForm').toggleClass('hidden');
        $('#resetForm').toggleClass('hidden');
        var isEmailFormVisible = $('#emailForm').is(':visible');
        $('#toggleForm').text(isEmailFormVisible ? 'Ver o formulário de redefinição de senha' : 'Ver o formulário de envio de e-mail');
      });

      $('#emailRecoveryForm').on('submit', function(event) {
        event.preventDefault();
        alert('Instruções enviadas para o e-mail!');
        $('#emailForm').addClass('hidden');
        $('#resetForm').removeClass('hidden');
      });

      $('#passwordResetForm').on('submit', function(event) {
        event.preventDefault();
        var newPassword = $('#new_password_field').val();
        var confirmPassword = $('#confirm_password_field').val();
        var valid = true;

        if (newPassword.length < 8) {
          $('#alert-password-policy').show();
          valid = false;
        }

        if (newPassword !== confirmPassword) {
          $('#alert-password-mismatch').show();
          valid = false;
        }

        if (valid) {
          $('#alert-success').show();
          setTimeout(function() {
            window.location.href = 'login.html'; // Redireciona para a tela de login após 3 segundos
          }, 3000);
        }
      });

      $('#btBackToEmailForm').on('click', function() {
        $('#resetForm').addClass('hidden');
        $('#emailForm').removeClass('hidden');
      });

      $('#btBackToLogin').on('click', function() {
        window.location.href = 'login.html'; // Redireciona para a tela de login
      });

      $(document).on('click', function(event) {
        if (!$(event.target).closest('.alert').length) {
          $('.alert').hide();
        }
      });
});