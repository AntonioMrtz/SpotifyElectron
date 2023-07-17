
export interface PropsInfoPopover{

  type : InfoPopoverType | undefined,
  response : InfoPopoverResponse | undefined,
  description : String | undefined,
  triggerOpenConfirmationModal : boolean
  /* handle closing the parent if needed */
  handleClose? : Function | undefined

}

export enum InfoPopoverType {
  PLAYLIST = 'Playlist',
  SONG = 'Canción',
  COMPARTIR_BUTTON ='Btn-Compartir'

}

export enum InfoPopoverResponse {
  ERROR = 'no se ha podido añadir',
  SUCCESS = 'se ha añadido correctamente',
}
