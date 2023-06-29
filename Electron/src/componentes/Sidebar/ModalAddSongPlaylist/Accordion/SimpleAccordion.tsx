import { ChangeEvent, ChangeEventHandler, FormEvent, FormEventHandler, Fragment } from 'react';
import Accordion from '@mui/material/Accordion';
import AccordionSummary from '@mui/material/AccordionSummary';
import AccordionDetails from '@mui/material/AccordionDetails';
import Typography from '@mui/material/Typography';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import LibraryMusicRoundedIcon from '@mui/icons-material/LibraryMusicRounded';
import AudiotrackIcon from '@mui/icons-material/Audiotrack';
import styles from './simpleAccordion.module.css';
import { useState,useRef } from 'react';

export default function SimpleAccordion() {

  const formRef = useRef<HTMLFormElement>(null);


  const [formData, setFormData] = useState({
    name: '',
    artist: '',
    genre:'',
    file:''
  });


  const handleChange = (event: ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {

    if(event.target && event.target.name ){

      setFormData({
        ...formData,
        [event.target.name]: event.target.value,
      });
    }
  };

  const handleChangeFile = (event: ChangeEvent<HTMLInputElement>) => {

    if(event.target && event.target.files ){

      let path :string = event.target.files[0].path

      setFormData({
        ...formData,
        [event.target.name]: event.target.value,
        file:path
      });


    }
  };

  const handleSubmitSong = (event:FormEvent<HTMLButtonElement>) => {

    event.preventDefault()

    if(formData){
      window.electron.submitSong.sendMessage('submit-song',formData)
    }

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
        <AccordionDetails className="p-4">

            <form className={`container-fluid d-flex flex-column p-0`} ref={formRef}>
              <div className={`container-fluid d-flex flex-row p-0`}>
                <div className="p-0 mb-3 me-3">
                  <input
                    type="text"
                    id="name"
                    name='name'
                    placeholder="Nombre de la cancion"
                    className={` ${styles.input}`}
                    onChange={handleChange}
                    required
                  ></input>
                </div>
                <div className="mb-3">
                  <input
                    type="text"
                    id="artist"
                    placeholder="Artista"
                    className={` ${styles.input}`}
                    onChange={handleChange}
                    name='artist'
                    required
                  ></input>
                </div>
              </div>
              <div className="p-0 mb-3 me-2">
                <input
                  type="text"
                  id="photo"
                  placeholder="URL de la miniatura"
                  className={` form-control w-75 ${styles.input}`}
                  onChange={handleChange}
                  name='photo'
                  required
                ></input>
              </div>

              <div className={`d-flex flex-row overflow-hidden align-items-center`}>
                <div className={`me-5`}>
                  <select
                    className="form-select-sm mb-3"
                    aria-label="Default select example"
                    onChange={handleChange}
                    name='genre'
                    required
                  >
                    <option className={` ${styles.option}`} defaultValue={"Pop"}>Pop</option>
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

              <button type="button" onClick={handleSubmitSong} className={`btn ${styles.btnSend}`}>Subir</button>

            </form>
        </AccordionDetails>
      </Accordion>
    </Fragment>
  );
}
