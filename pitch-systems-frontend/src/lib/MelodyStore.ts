import Melody from '$lib/Melody';

/**
 * Abstract class to store Melody objects.
 */
abstract class MelodyStore {

    /**
     * Add a melody to the storage, or update it if it already exists.
     * @param key 
     * @param value 
     * @return boolean Depending on success.
     */
    abstract save(melody: Melody): boolean

    /**
     * Get an item from storage, if it exists.
     * @param id 
     * @return Melody
     */
    abstract get(id: string): Melody

    /**
     * 
     * @param key 
     */
    abstract remove(id: string): boolean

    /**
     * Get a list of stored items
     * 
     
     */
    abstract list(): string[]

}

export class MelodyLocalStorage extends MelodyStore {
    
    //Use an internal property as proxy for the localStorage list so server-side rendering also works.
    protected melodies: string[];

    constructor() {
        super();

        try {
            let list_string = localStorage.getItem("audio_list");
            this.melodies = list_string ? JSON.parse(list_string) : []
        } catch {
            this.melodies = []
        }
    }

    save(melody: Melody) {
        
        //New entry
        if (this.melodies.indexOf(melody.id) == -1) {
            this.melodies.push(melody.id)
        }

        try {
            localStorage.setItem("audio_list", JSON.stringify(this.melodies));
            localStorage.setItem(melody.id, JSON.stringify(melody));
            return true;
        } catch (error) {
            console.warn("Can't add to local storage");
            console.warn(error);
            return false;
        }
    }

    get(id: string) {
        const data = localStorage.getItem(id)

        if (data == null) {
            throw new Error("Invalid id requested");
        }

        const obj = JSON.parse(data);
        console.log(obj);
        const melody = new Melody(obj.id, obj.name, obj.path);
        for (const [k,v] of Object.entries(obj)) {
            if (melody.hasOwnProperty(k)) melody[k] = v //Tidy up typing here
        }
        return melody;
    }

    remove(id: string) {
        const index = this.melodies.indexOf(id);
        if (index == -1) {
            return false;
        }
        this.melodies.splice(index);

        localStorage.setItem("audio_list", JSON.stringify(this.melodies));
        localStorage.removeItem(id);
        return true;
    }

    list() {
        return this.melodies;
    }

    refresh() {
        const list = localStorage.getItem("audio_list");
        if (list) {
            this.melodies = JSON.parse(list);
        } else {
            this.melodies = [];
        }
    }
}