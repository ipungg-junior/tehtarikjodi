class ElementManager {
    constructor(elementId) {
        this.element = document.getElementById(elementId);
    }

    setText(text) {
        this.element.textContent = text;
    }

    click(callbackFunction) {
        this.element.addEventListener('click', callbackFunction);
    }

    hover(callbackFunction) {
        this.element.addEventListener('hover', callbackFunction);
    }

    getValue(){
        return this.element.value;
    }
}


class HttpManager {
    constructor(uri){
        this.uri = uri;
        this.header = {};
        this.form = new FormData();
        this.data = '';
    }

    async post(onSuccess=null, onError=null){
        try {
            const response = await fetch(this.uri, {method: 'POST', headers:this.header, body:this.form});

            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            const data = await response.json();
            return data;
        } catch (error) {
            return error.message;
        }
    }

    setData(key, value){
        this.form.append(key, value);
    }

    setHeader(key, value){
        this.header[key] = value;
    }

}