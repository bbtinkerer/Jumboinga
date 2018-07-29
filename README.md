# Jaboinga - The Jumping Boinging Game

By bbtinkerer (<http://bb-tinkerer.blogspot.com/>)

## Description

Simple roulette/wheel type game using a door stop spring to spin the wheel. Uses the Adafruit Circuit Playground Express (CPX) with a piezoelectric sensor and a door stop spring. User pulls back on the door stop spring and lets go (or knocks the game board really hard) to start the wheel moving (light going around the NeoPixel ring of the CPX). Wheel spin determined by how strong and long the spring vibrates.

Instructions for building the game board are found at [Instructables.com](https://www.instructables.com/id/Jumboinga-the-Jumping-Boinging-Game).

Video on [Youtube.com](https://youtu.be/6GT_mvp9cMk)

## Requirements

* [Circuit Playground Express](https://learn.adafruit.com/adafruit-circuit-playground-express?view=all) - Follow instructions on setup. This game requires CircuitPython v3.

## Installation

Follow the instructions at Adafruit to copy the following files to the Circuit Playground Express:

* code.py
* 110317__timbre__remix-of-62176-fanfare-before-after.wav
* 234565__foolboymedia__announcement-begin.wav
* 320883__rhodesmas__action-03.wav
* 362204__taranp__horn-fail-wahwah-3.wav

## Configuration

There are some settings towards the top of code.py. Most important are the VIBRATION_READ_TIME_XXX_THREHOLD variables.
 
Short threshold is the minimum value to trigger the game. Choose a value a bit higher than the noise piezo picks up and the slightest bumps. Take note of the value.

Set Medium and Long threshold to 66000. Trigger the spring as hard as it will go and adjust the Short threshold. Find the value that triggers the strongest vibrations. Then knock off a thousand or couple hundred off that value. Set Long threshold to that value. Set Short threshold to the value you found earlier.

The rest of the configurable settings are documented in the comments.

## Acknowledgements

The CC licensed sounds are from [freesound.org](https://freesound.org):

* [110317__timbre__remix-of-62176-fanfare-before-after.wav](https://freesound.org/people/Timbre/sounds/110317/) by [Timbre](https://freesound.org/people/Timbre/)
* [234565__foolboymedia__announcement-begin.wav](https://freesound.org/people/FoolBoyMedia/sounds/234565/) by [FoolBoyMedia](https://freesound.org/people/FoolBoyMedia/)
* [320883__rhodesmas__action-03.wav](https://freesound.org/people/rhodesmas/sounds/320883/) by [rhodesmas](https://freesound.org/people/rhodesmas/)
* [362204__taranp__horn-fail-wahwah-3.wav](https://freesound.org/people/TaranP/sounds/362204/) by [TaranP](https://freesound.org/people/TaranP/)

My wife for putting up with the constant boing'ing during the making of this game.

## Known Issues

If you discover any bugs, feel free to create an issue on GitHub fork and
send a pull request.


## Authors

* bbtinkerer (https://github.com/bbtinkerer/)


## Contributing

1. Fork it
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create new Pull Request


## License

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.