window.addEventListener("load", (event) => {
    const inputPhoto = document.querySelector('#id_photo');

    const newPhoto = document.querySelector('.photo-img-new');

    const newPhotoDiv = document.querySelector('.photo-image-new');

    const form = document.querySelector('form');

    const cropper_photo = new Cropper(newPhoto, {
        aspectRatio: 1 / 1,
        crop(event) {},
    });

    inputPhoto.addEventListener('change', function() {
        const file = inputPhoto.files[0];

        if (file) {
            const reader = new FileReader();

            reader.addEventListener('load', function() {
                newPhoto.src = reader.result;
                newPhoto.style.display = 'block';
                newPhotoDiv.style.display = 'flex';

                let imageURL = URL.createObjectURL(file);
                cropper_photo.destroy();
                cropper_photo.replace(imageURL);

                $('form#change-profile').submit(function(event) {
                    event.preventDefault();
                    const form = this;
                    cropper_photo.getCroppedCanvas().toBlob((blob) => {
                        const fd = new FormData(form);
                        const newPhotoFile = new File([blob], `photo.${blob.type.split('/')[1]}`, { type: blob.type });
                        fd.set('photo', newPhotoFile);

                        $.ajax({
                            type: 'POST',
                            url: $(this).action,
                            enctype: 'multipart/form-data',
                            data: fd,
                            success: function(response) {
                            console.log(response[0]);
                            console.log(response.href);
                                window.location.href = response.url;
                            },
                            error: function(error) {
                            },
                            cache: false,
                            contentType: false,
                            processData: false,
                        });
                    });
                });
            });

            reader.readAsDataURL(file);
        }
    });
});