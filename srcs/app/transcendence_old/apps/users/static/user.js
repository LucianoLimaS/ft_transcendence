    $(document).ready(function () {
        $('#editButton').on('click', function (event) {
            event.preventDefault();

            if ($(this).text() === 'Editar') {
                $(this).removeClass('btn-warning').addClass('btn-success').text('Salvar');
                $('#uploadImage').css('display', 'block');
                $('#userNameField').prop('readonly', false);
                $('#nicknameField').prop('readonly', false);
                $('#emailField').prop('readonly', false);
                $('#passwordField').prop('readonly', false);
                $('#confirmPasswordField').prop('readonly', false)
                $('#confirmPasswordDiv').css('display', 'block');
                $('#descriptionField').prop('readonly', false);
            } else {
                if ($('#passwordField').val() !== $('#confirmPasswordField').val()) {
                    alert('As senhas não conferem.');
                }
                else if ($('#userNameField').val() === '') {
                    alert('O nome não pode ser vazio.');
                }
                else {
                    $(this).removeClass('btn-success').addClass('btn-warning').text('Editar');
                    $('#uploadImage').css('display', 'none');
                    $('#userNameField').prop('readonly', true);
                    $('#nicknameField').prop('readonly', true);
                    $('#emailField').prop('readonly', true);
                    $('#passwordField').prop('readonly', true);
                    $('#confirmPasswordField').prop('readonly', true)
                    $('#confirmPasswordDiv').css('display', 'none');
                    $('#descriptionField').prop('readonly', true);

                    // Chamar ajax se necessário
                }
            }
        });
    }); 