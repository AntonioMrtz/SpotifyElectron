import { useState, useEffect } from 'react';
import styles from '../addSongPlayListAccordion.module.css';

interface PropsGenreOption {
  name: any;
  value: any;
}

export default function GenreOption(props: PropsGenreOption) {
  const [name, setName] = useState<string>('');
  const [value, setValue] = useState<string>('');

  useEffect(() => {
    if (props.name && props.value) {
      setName(props.name);
      setValue(props.value);
    }
  }, [props]);

  return (
    <option className={` ${styles.option}`} value={value}>
      {name}
    </option>
  );
}
