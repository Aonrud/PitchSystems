import Melody from '$lib/Melody';

/**
 * Abstract class to store Melody objects.
 */
abstract class MelodyStore {

    /**
     * Add an item to the storage
     * @param key 
     * @param value 
     * @return boolean Depending on success.
     */
    abstract add(melody: Melody): boolean

    /**
     * Get an item from storage.
     * @param id 
     * @return Melody
     */
    abstract get(id: string): Melody
    /**
     * 
     * @param key 
     * @param value 
     */
    abstract update(id: string, melody: Melody): boolean

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

    add(melody: Melody) {
        this.melodies.push(melody.id);
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
        if (data !== null) {
            return JSON.parse(data);
        }
    }

    update(id: string, melody: Melody) {
        const index = this.melodies.indexOf(id);
        if (index == -1) {
            return false;
        }
        localStorage.setItem(id, JSON.stringify(melody));
        return true;
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
        }
    }
}