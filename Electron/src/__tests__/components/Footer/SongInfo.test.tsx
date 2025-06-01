import '@testing-library/jest-dom';
import { fireEvent, render } from '@testing-library/react';
import SongInfo from 'components/footer/SongInfo/SongInfo';
import { BrowserRouter } from 'react-router-dom';
import { act } from 'react';

test('Render Song info', () => {
  const component = render(
    <BrowserRouter>
      <SongInfo name="" thumbnail="" artist="" />
    </BrowserRouter>,
  );
  expect(component).toBeTruthy();
});

test('Song info click like', async () => {
  const component = render(
    <BrowserRouter>
      <SongInfo name="" thumbnail="" artist="" />
    </BrowserRouter>,
  );

  const buttonLike = component.queryByTestId('songinfo-like-button');

  await act(() => {
    if (buttonLike) {
      return fireEvent.click(buttonLike);
    }

    return null;
  });

  expect(buttonLike).not.toBeInTheDocument();
});

test('Song info click unlike', async () => {
  const component = render(
    <BrowserRouter>
      <SongInfo name="" thumbnail="" artist="" />
    </BrowserRouter>,
  );

  const buttonLike = component.queryByTestId('songinfo-like-button');

  await act(() => {
    if (buttonLike) {
      return fireEvent.click(buttonLike);
    }

    return null;
  });

  const buttonUnLike = component.queryByTestId('songinfo-unlike-button');

  await act(() => {
    if (buttonUnLike) {
      return fireEvent.click(buttonUnLike);
    }

    return null;
  });

  expect(buttonUnLike).not.toBeInTheDocument();
});
