class AudioParser {
    PARSER_SOCKET = "ws://localhost:5678";
    socket: WebSocket;
    ready: boolean = false;

    constructor() {
        const socket = new WebSocket(this.PARSER_SOCKET)
        socket.addEventListener("open", this.setReady)
        socket.addEventListener("message", this.message)
        this.socket = socket
    }

    setReady() {
        this.ready = true;
    }

    message() {
        dispatchEvent(new CustomEvent("message"))
    }

    async sendURL(url: string) {
        if (!this.ready) {
            return Error("Not ready")
        }
        const message = JSON.stringify({ "url": url });
        this.socket.send(message);
    }
}

export default AudioParser