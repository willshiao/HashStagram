// multiple pngs (up to 3) accepted without spitting out error message
FilePond.setOptions({
  // allowBrowse: false,
  acceptedFileTypes: ['image/png', 'image/jpeg', 'image/jpg', 'image/bmp'],
  maxFileSize: '10MB',
  maxTotalFileSize: '10MB',
  maxFiles: 1
})

const pond = FilePond.create(document.querySelector('input.filepond'))

// We want to preview images, so we register
// the Image Preview plugin, We also register 
// exif orientation (to correct mobile image
// orientation) and size validation, to prevent
// large files from being added
FilePond.registerPlugin(
  FilePondPluginImagePreview,
  FilePondPluginImageExifOrientation,
  FilePondPluginFileValidateType,
  FilePondPluginImageValidateSize,
  FilePondPluginFileValidateSize
)

function postData (url, file) {
  // Default options are marked with *
  const formData = new FormData()

  formData.append('photo', file)

  return fetch (url, {
    method: 'POST',
    body: formData
  })
    .then((response) => {
      console.log(response)
      return Promise.resolve(response)
      // now put response on the picture (see below, line 51 or so)
    })
    .catch(err => {
      console.error(err)
    })
}

$(function () {
  let formDisabled = false

  $('#upload-btn').click(function (evt) {
    evt.preventDefault()
    if (formDisabled) return false

    console.log('Button pressed!')
    formDisabled = true
    $('#upload-btn').addClass('disabled')
    const f = pond.getFile().file

    postData('/api/upload', f)
      .then(res => {
        if (res.status !== 200) {
          $('#img-caption').text('An error occurred: ', res.statusText)
          formDisabled = false
          $('#upload-btn').removeClass('disabled')
          return
        }

        res.json()
          .then(resData => {
            console.log('Got response from Jerry :)', resData)
            const reader = new FileReader()
            reader.readAsDataURL(f)

            reader.onload = function (evt) {
              if (evt.target.readyState == FileReader.DONE) {
                const hashtagText = resData.data
                  .map(tag => `<a href="https://www.instagram.com/explore/tags/${tag}/" class="badge badge-primary hashtag">#${tag}</a>`)
                  .join(' ')

                $('#image-info').html(`
                <img class="card-img-top" src="${evt.target.result}" alt="Card image cap">
                <div class="card-body">
                  <p class="card-text">${hashtagText}</p>
                </div>
                `)

                formDisabled = false
                $('#upload-btn').removeClass('disabled')
              }
            }
          })
      })

  })
})

// postData(`https://us-central1-sdhacksproject2018.cloudfunctions.net/dummy`, {answer: 42})
// // find 'image data' variable; also, how to link this behavior to button in index.html?
// .then(data => console.log(JSON.stringify(data))) // JSON-string from `response.json()` call
// .catch(error => console.error(error));



