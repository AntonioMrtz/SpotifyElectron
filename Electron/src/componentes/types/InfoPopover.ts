export enum InfoPopoverType {
  ERROR = 'ERROR',
  SUCCESS = 'SUCCESS',
  CLIPBOARD = 'CLIPBOARD',
}
export interface PropsInfoPopover {
  title: string | undefined;
  description: String | undefined;
  type: InfoPopoverType | undefined;
  triggerOpenConfirmationModal: boolean;
  /* handle closing the parent if needed */
  handleClose?: Function | undefined;
}
