import { fail } from '@sveltejs/kit'
import { writeFile } from 'fs/promises'
import { randomUUID } from 'crypto'

const STATIC_DIR = 'static'
const CACHE_DIR = 'cache'

export const actions = {
  upload: async ({ request }) => { 
    const data = await request.formData();
    const file = data.get('audio_file') as File;

    if (
      !file.name ||
      file.name === 'undefined'
    ) {
      return fail(400, {  
        error: true,
        message: 'You must provide a file to upload'
      });
    }

    const id: string = randomUUID()
    const ext: string|undefined = file.name.split('.').pop()
    const path = `${CACHE_DIR}/${id}.${ext}`
    
    //cache the file
    await writeFile(`${STATIC_DIR}/${path}`, new Uint8Array(await file.arrayBuffer()));

    let name = ( file.name.lastIndexOf(".") > 0 ? file.name.substring(0, file.name.lastIndexOf(".")) : file.name );
    name = name.replaceAll(/[_-]+/g," ") //Swap typical space-replacing chars in the filename

    console.log(path);
    return {
      success: true,
      file: {
        "uuid": id,
        "name": name,
        "path": path
      }
    };
  },
  delete: async ({ request }) => { 
    //STUB
  }
};