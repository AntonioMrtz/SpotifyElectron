export function secondsToHoursAndMinutesFormatted(seconds: number) {
  const hours = Math.floor(seconds / 3600);
  const remainingSeconds = seconds % 3600;
  const minutes = Math.floor(remainingSeconds / 60);

  return `${hours} h ${minutes} min `;
}

export const secondsToMinutesSeconds = (secondsInput: number) => {
  const minutes = Math.floor(secondsInput / 60);
  const seconds = (secondsInput - minutes * 60) / 100;

  return (minutes + seconds).toFixed(2).replace('.', ':');
};
