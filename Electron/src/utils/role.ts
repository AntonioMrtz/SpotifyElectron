export enum UserType {
  USER = 'usuario',
  ARTIST = 'artista',
}

export const backendPathFromUserType: Record<UserType | string, string> = {
  [UserType.ARTIST]: 'artistas',
  [UserType.USER]: 'usuarios',
};
