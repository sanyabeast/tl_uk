const { ipcRenderer } = require('electron');
console.log('preload script loading...')
let dom_loaded = false

ipcRenderer.on('get_translation', async (event, data) => {
    // do something with the data
    console.log(data);
    await when_page_ready()
    console.log('page_ready')

    let translation = await get_translation(data)
    console.log(translation)

    ipcRenderer.send('get_translation.response', {
        translation: translation
    })
});


window.addEventListener('DOMContentLoaded', () => {
    dom_loaded = true;
});

function when_page_ready() {
    return new Promise((resolve, reject) => {
        let started_at = +new Date()
        let id = setInterval(() => {
            if (dom_loaded && document.querySelectorAll('textarea').length > 0) {
                resolve(true)
                clearInterval(id)
            }

            if (+new Date() - started_at > 30 * 1000) {
                reject()
            }
        }, 500)
    })
}

function get_translation(params) {
    return new Promise((resolve, reject) => {
        let frame = document.createElement('iframe')
        frame.src = `https://translate.google.com/?sl=${params.from_language}&tl=${params.to_language}&text=${params.text}&op=translate`
        frame.style.position = 'fixed'
        frame.style.top = '0'
        frame.style.left = '0'
        frame.style.zIndex = '999'
        frame.style.width = '100%'
        frame.style.height = '100%'

        let started_at = +new Date()
        let id = setInterval(() => {
            let translated = frame.contentWindow.document.querySelector('div[aria-live="polite"] span:first-child span:first-child span:first-child')
            console.log(translated)
            if (translated != null) {
                clearInterval(id)
                setTimeout(() => {
                    resolve(translated.textContent)
                    frame.remove()
                }, 500)
            }

            if (+new Date() - started_at > 30 * 1000) {
                reject()
                clearInterval(id)
                frame.remove()
            }
        }, 500)

        document.body.appendChild(frame)

    })
}