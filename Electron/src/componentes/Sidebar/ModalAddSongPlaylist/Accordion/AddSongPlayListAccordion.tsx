import { ChangeEvent, ChangeEventHandler, FormEvent, FormEventHandler, Fragment } from 'react';
import Accordion from '@mui/material/Accordion';
import AccordionSummary from '@mui/material/AccordionSummary';
import AccordionDetails from '@mui/material/AccordionDetails';
import Typography from '@mui/material/Typography';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import LibraryMusicRoundedIcon from '@mui/icons-material/LibraryMusicRounded';
import AudiotrackIcon from '@mui/icons-material/Audiotrack';
import styles from './addSongPlayListAccordion.module.css';
import { useState,useRef } from 'react';


interface PropsSimpleAccordion{

  handleClose : Function

}

export default function SimpleAccordion(props:PropsSimpleAccordion) {

  const [songFile,setSongFile] = useState<File>()

  const [thumbnailUpload,setThumbnailUpload] = useState<string>()

  const [formData, setFormData] = useState({
    nombre: '',
    artista: '',
    genero:'',
    foto:'',
  });


  const handleChange = (event: ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {

    if(event.target && event.target.name ){

      if(event.target.name==="foto"){

        setThumbnailUpload(event.target.value)
      }

      setFormData({
        ...formData,
        [event.target.name]: event.target.value,
      });
    }
  };

  const handleChangeFile = (event: ChangeEvent<HTMLInputElement>) => {

    if(event.target && event.target.files ){

      setSongFile(event.target.files[0])

    }
  };

  const handleSubmitSong = (event:FormEvent<HTMLButtonElement>) => {

    const backendBasePath = new URL("http://127.0.0.1:8000/");

    let url = new URL(backendBasePath + 'canciones/');

    event.preventDefault()


    if(formData && songFile){
      //window.electron.submitSong.sendMessage('submit-song',formData)

      for (let [key, value] of Object.entries(formData)) {
        if (key !== 'file' && typeof value === 'string') {
          url.searchParams.set(key, value);
        }
      }
      const formDataFile = new FormData();
      formDataFile.append('file', songFile);


      const requestOptions = {
        method: 'POST',
        body:formDataFile

      };

      fetch(url, requestOptions)
        .then((response) =>

          {

            if(response.status==201){

              console.log("Cancion creada")

            }else{

              console.log("No se a creado la cancion")
            }
          }

        )
        .catch((error) => {
          console.error('Error:', error);
        });
    }

    props.handleClose()

    //formRef.current?.submit()
  };




  return (
    <Fragment>
      <Accordion
        style={{
          backgroundColor: 'var(--secondary-black)',
          borderColor: '#ffffff',
        }}
      >
        <AccordionSummary
          expandIcon={<ExpandMoreIcon />}
          aria-controls="panel1a-content"
          id="panel1a-header"
          style={{ border: '1px solid var(--primary-black)' }}
        >
          <Typography
            style={{
              color: 'var(--primary-green)',
              fontWeight: '700',
              textTransform: 'uppercase',
            }}
          >
            <LibraryMusicRoundedIcon /> Crear lista de reproducción
          </Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Typography style={{ color: 'var(--primary-white' }}>
            {' '}
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse
            malesuada lacus ex, sit amet blandit leo lobortis eget.
          </Typography>
        </AccordionDetails>
      </Accordion>

      <Accordion
        style={{
          backgroundColor: 'var(--secondary-black)',
          borderColor: '#ffffff',
        }}
      >
        <AccordionSummary
          expandIcon={<ExpandMoreIcon />}
          aria-controls="panel1a-content"
          id="panel1a-header"
          style={{ border: '1px solid var(--primary-black)' }}
        >
          <Typography
            style={{
              color: 'var(--primary-green)',
              fontWeight: '700',
              textTransform: 'uppercase',
            }}
          >
            <AudiotrackIcon /> Subir canción
          </Typography>
        </AccordionSummary>
        <AccordionDetails className={`p-4 d-flex flex-row ${styles.accordionDetails}`}>

            <form className={`container-fluid d-flex flex-column p-0 ${styles.formAddSong}`}>
              <div className={`container-fluid d-flex flex-row p-0`}>
                <div className="p-0 mb-3 me-3">
                  <input
                    type="text"
                    id="nombre"
                    name='nombre'
                    placeholder="Nombre de la cancion"
                    className={` ${styles.input}`}
                    onChange={handleChange}
                    required
                  ></input>
                </div>
                <div className="mb-3">
                  <input
                    type="text"
                    id="artista"
                    placeholder="Artista"
                    className={` ${styles.input}`}
                    onChange={handleChange}
                    name='artista'
                    required
                  ></input>
                </div>
              </div>
              <div className="p-0 mb-3 me-2">
                <input
                  type="text"
                  id="foto"
                  placeholder="URL de la miniatura"
                  className={` form-control ${styles.input}`}
                  onChange={handleChange}
                  name='foto'
                  required
                ></input>
              </div>

              <div className={`d-flex flex-row overflow-hidden align-items-center ${styles.containerSelectAndFileSelector}`}>
                <div className={`me-5`}>
                  <select
                    className="form-select-sm mb-3"
                    aria-label="Default select example"
                    onChange={handleChange}
                    name='genero'
                    required
                    defaultValue={"Elige un género"}
                  >
                    <option className={` ${styles.option}`} value={"Elige un género"} disabled>❗ Elige un género</option>
                    <option className={` ${styles.option}`} value={"Pop"}>Pop</option>
                    <option className={` ${styles.option}`} value="Rock">Rock</option>
                    <option className={` ${styles.option}`} value="Hip-hop">Hip-hop</option>
                    <option className={` ${styles.option}`} value="R&B (Ritmo y Blues)">
                      R&B (Ritmo y Blues)
                    </option>
                    <option className={` ${styles.option}`}value="Jazz">Jazz</option>
                    <option className={` ${styles.option}`} value="Blues">Blues</option>
                    <option className={` ${styles.option}`} value="Reggae">Reggae</option>
                    <option className={` ${styles.option}`} value="Country">Country</option>
                    <option className={` ${styles.option}`} value="Folk">Folk</option>
                    <option className={` ${styles.option}`} value="Clásica">Clásica</option>
                    <option className={` ${styles.option}`} value="Electrónica">Electrónica</option>
                    <option className={` ${styles.option}`} value="Dance">Dance</option>
                    <option className={` ${styles.option}`} value="Metal">Metal</option>
                    <option className={` ${styles.option}`} value="Punk">Punk</option>
                    <option className={` ${styles.option}`} value="Funk">Funk</option>
                    <option className={` ${styles.option}`} value="Soul">Soul</option>
                    <option className={` ${styles.option}`} value="Gospel">Gospel</option>
                    <option className={` ${styles.option}`} value="Latina">Latina</option>
                    <option className={` ${styles.option}`} value="Música del mundo">Música del mundo</option>
                    <option className={` ${styles.option}`} value="Experimental">Experimental</option>
                    <option className={` ${styles.option}`} value="Ambiental">Ambiental</option>
                    <option className={` ${styles.option}`} value="Fusión">Fusión</option>
                    <option className={` ${styles.option}`} value="Instrumental">Instrumental</option>
                    <option className={` ${styles.option}`} value="Alternativa">Alternativa</option>
                    <option className={` ${styles.option}`} value="Indie">Indie</option>
                    <option className={` ${styles.option}`} value="Rap">Rap</option>
                    <option className={` ${styles.option}`} value="Ska">Ska</option>
                    <option className={` ${styles.option}`} value="Grunge">Grunge</option>
                    <option className={` ${styles.option}`} value="Trap">Trap</option>
                    <option className={` ${styles.option}`} value="Reggaeton">Reggaeton</option>
                  </select>
                </div>
                <div className="mb-3">
                  <input
                  className={`form-control-md ${styles.input}`}
                    type="file"
                    id="file"
                    name='file'
                    onChange={handleChangeFile}
                    accept="audio/mp3"
                    required
                  ></input>
                </div>
              </div>


                <button type="button" onClick={handleSubmitSong} className={`btn btn-lg ${styles.btnSend}`}>Subir</button>

            </form>

            <div className={`${styles.containerThumbNailUpload}`}><img className='img-fluid' src={thumbnailUpload} alt="" /></div>
        </AccordionDetails>
      </Accordion>
    </Fragment>
  );
}
