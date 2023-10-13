import styles from '../addSongPlayListAccordion.module.css';

interface PropsGenreOption {
  name: string;
  value: string;
}

export default function GenreOption({ name, value }: PropsGenreOption) {
  return (
    <option className={` ${styles.option}`} value={value}>
      {name}
    </option>
  );
}
