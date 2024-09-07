import { Genre } from '../swagger/api';

export const genreColorsMapping: Record<string, string> = {
  [Genre.POP]: '#FF3300', // Rojo oscuro
  [Genre.ROCK]: '#0055AA', // Azul oscuro
  [Genre.HIP_HOP]: '#FFA200', // Naranja oscuro
  // eslint-disable-next-line no-underscore-dangle
  [Genre.R_B_RITMO_Y_BLUES_]: '#6600AA', // Morado oscuro
  [Genre.JAZZ]: '#228833', // Verde oscuro
  [Genre.BLUES]: '#004488', // Azul oscuro
  [Genre.REGGAE]: '#AA0033', // Rojo oscuro
  [Genre.COUNTRY]: '#AA0033', // Rojo oscuro (mismo que Reggae)
  [Genre.FOLK]: '#883322', // Marrón oscuro
  [Genre.CL_SICA]: '#226622', // Verde oscuro
  [Genre.ELECTR_NICA]: '#44AA22', // Verde oscuro
  [Genre.DANCE]: '#FF6600', // Naranja oscuro
  [Genre.METAL]: '#AA0044', // Rojo oscuro
  [Genre.PUNK]: '#992200', // Marrón oscuro
  [Genre.FUNK]: '#33AA33', // Verde oscuro
  [Genre.SOUL]: '#5500AA', // Morado oscuro
  [Genre.GOSPEL]: '#AA55AA', // Morado oscuro
  [Genre.LATINA]: '#00AAAA', // Cian oscuro
  [Genre.M_SICA_DEL_MUNDO]: '#66AA55', // Verde oscuro
  [Genre.EXPERIMENTAL]: '#AA5544', // Rojo oscuro
  [Genre.AMBIENTAL]: '#333333', // Gris oscuro
  [Genre.FUSI_N]: '#663344', // Marrón oscuro
  [Genre.INSTRUMENTAL]: '#220033', // Morado oscuro
  [Genre.ALTERNATIVA]: '#AA00AA', // Morado oscuro
  [Genre.INDIE]: '#880088', // Morado oscuro
  [Genre.RAP]: '#0000AA', // Azul oscuro
  [Genre.SKA]: '#AA0000', // Rojo oscuro
  [Genre.GRUNGE]: '#AAAA00', // Amarillo oscuro
  [Genre.TRAP]: '#00AA00', // Verde oscuro
  [Genre.REGGAETON]: '#00AAAA', // Cian oscuro
};

export function getGenreFromString(genreName: string) {
  const genre = Object.values(Genre).find((x) => x === genreName);
  if (!genre) {
    throw new Error(`Cannot get Genre from ${genreName}`);
  }

  return genre;
}
