class AudioParser {
    PARSER_API = "http://localhost:5000/api/v1/"
    
    source: string

    constructor(source: string) {
        this.source = encodeURIComponent(source)
    }

    async parse() {
        const response = await fetch(`${this.PARSER_API}?url=${this.source}`)
        return await response.json()
    }
}

export default AudioParser