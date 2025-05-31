import '@testing-library/jest-dom';
import '@testing-library/jest-dom/extend-expect';
import { fireEvent, render } from '@testing-library/react';
import { act } from 'react';

import SongConfig from 'components/footer/SongConfig/SongConfig';
import VolumeSlider from 'components/footer/SongConfig/VolumeSlider/VolumeSlider';
import { BrowserRouter } from 'react-router-dom';

test('Render Song Config', () => {
  const mockChangeVolume = jest.fn();

  const component = render(
    <BrowserRouter>
      <SongConfig changeVolume={mockChangeVolume} />
    </BrowserRouter>,
  );
  expect(component).toBeTruthy();
});

test('Render Volume Slider', () => {
  const mockChangeVolume = jest.fn();

  const component = render(
    <BrowserRouter>
      <VolumeSlider changeVolume={mockChangeVolume} />
    </BrowserRouter>,
  );
  expect(component).toBeTruthy();
});

test('Song config change volume', async () => {
  const mockChangeVolume = jest.fn();

  const component = render(
    <BrowserRouter>
      <VolumeSlider changeVolume={mockChangeVolume} />
    </BrowserRouter>,
  );

  const slider = component.container.querySelector('input[type="range"]');

  await act(async () => {
    if (slider) {
      fireEvent.change(slider, { target: { value: 25 } });
    }
  });

  expect(mockChangeVolume).toHaveBeenCalledWith(25);
});

test('Song config change volume to 0', async () => {
  const mockChangeVolume = jest.fn();

  const component = render(
    <BrowserRouter>
      <VolumeSlider changeVolume={mockChangeVolume} />
    </BrowserRouter>,
  );

  const slider = component.container.querySelector('input[type="range"]');

  await act(async () => {
    if (slider) {
      fireEvent.change(slider, { target: { value: 0 } });
    }
  });

  expect(mockChangeVolume).toHaveBeenCalledWith(0);
  expect(
    component.getByTestId('songconfig-speaker-button-mute'),
  ).toBeInTheDocument();
});

test('Volume Slider click mute', async () => {
  const mockChangeVolume = jest.fn();

  const component = render(
    <BrowserRouter>
      <VolumeSlider changeVolume={mockChangeVolume} />
    </BrowserRouter>,
  );

  const speakerButton = component.getByTestId('songconfig-speaker-button');

  await act(() => {
    return fireEvent.click(speakerButton);
  });

  expect(
    component.getByTestId('songconfig-speaker-button-mute'),
  ).toBeInTheDocument();
});
