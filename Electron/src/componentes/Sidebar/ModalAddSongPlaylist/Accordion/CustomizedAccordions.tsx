import { Fragment } from 'react';
import Accordion from '@mui/material/Accordion';
import AccordionSummary from '@mui/material/AccordionSummary';
import AccordionDetails from '@mui/material/AccordionDetails';
import Typography from '@mui/material/Typography';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';

export default function SimpleAccordion() {
  return (

    <Fragment>
      <Accordion style={{backgroundColor:"var(--secondary-black)",borderColor:'#ffffff'}}>
        <AccordionSummary
          expandIcon={<ExpandMoreIcon />}
          aria-controls="panel1a-content"
          id="panel1a-header"
          style={{border:'1px solid var(--primary-black)'}}
        >
          <Typography style={{color:"var(--primary-green)",fontWeight:'700'}}>AÑADIR CANCIÓN</Typography>
        </AccordionSummary>
        <AccordionDetails>
        <Typography style={{color:'var(--primary-white'}}>            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse
            malesuada lacus ex, sit amet blandit leo lobortis eget.
          </Typography>
        </AccordionDetails>
      </Accordion>
      <Accordion style={{backgroundColor:"var(--secondary-black)"}}>
        <AccordionSummary
          expandIcon={<ExpandMoreIcon />}
          aria-controls="panel1a-content"
          id="panel1a-header"
        >
          <Typography style={{color:"var(--primary-green)",fontWeight:'700'}}>CREAR LISTA</Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Typography style={{color:'var(--primary-white'}}>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse
            malesuada lacus ex, sit amet blandit leo lobortis eget.
          </Typography>
        </AccordionDetails>
      </Accordion>

    </Fragment>


  );
}
