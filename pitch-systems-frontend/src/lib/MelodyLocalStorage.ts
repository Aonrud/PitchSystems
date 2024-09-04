import Melody from '$lib/Melody';

export class MelodyLocalStorage {

    static save(melody: Melody) {

        const list = MelodyLocalStorage.list()
        localStorage.setItem(melody.id, JSON.stringify(melody));

        //If this is a new item and not an update, add it to the list
        if (list.indexOf(melody.id) == -1) {
            list.push(melody.id);
            localStorage.setItem("saved-analyses", JSON.stringify(list))
        }
    }

    static get(id: string) {
        const data = localStorage.getItem(id)

        if (data == null) {
            return null;
        }

        const obj = JSON.parse(data);

        //The melody object has to be reconstructed so that it includes the melody class methods as well as properties.
        const melody = new Melody(obj.id, obj.name, obj.path);
        for (const [k, v] of Object.entries(obj)) {
            // @ts-ignore 
            if (melody.hasOwnProperty(k)) melody[k] = v
        }
        return melody;
    }

    static getAll() {
        const ids = MelodyLocalStorage.list();
        const list: Melody[] = [];

        for (const id of ids) {
            const melody = MelodyLocalStorage.get(id);
            if (melody) { //.get() can return null if there's a mismatch between the list and the records.
                list.push(melody);
            }
        }
        return list;
    }

    static remove(id: string) {
        const list = MelodyLocalStorage.list()
        const index = list.indexOf(id)
        if (index == -1) {
            return false;
        }

        list.splice(index);
        localStorage.setItem("saved-analyses", JSON.stringify(list));
        localStorage.removeItem(id);
        return true;
    }

    /**
     * Get a list of stored melodies
     * 
     * @returns string[]
     */
    static list() {
        const saved = localStorage.getItem("saved-analyses");
        if (saved) {
            return JSON.parse(saved)
        }
        return [];
    }

}