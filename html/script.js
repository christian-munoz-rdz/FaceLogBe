let userExampleInRgbaArray = [];
let userToFindInRgbaArray = [];

window.onload = function () {
  // user example
  const canvas = document.getElementById('miCanvas');
  const ctx = canvas.getContext('2d');

  const img = new Image();
  img.onload = function () {
    ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
    const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
    const data = imageData.data;

    userExampleInRgbaArray = [];
    for (let i = 0; i < data.length; i += 4) {
      const red = data[i];
      const green = data[i + 1];
      const blue = data[i + 2];
      const alpha = data[i + 3];
      userExampleInRgbaArray.push([red, green, blue, alpha]);
    }
    console.log(userExampleInRgbaArray);
  };
  img.src = 'maria4.jpg';

  // userToFind
  const canvasToFind = document.getElementById('findCanvas');
  const ctx2 = canvasToFind.getContext('2d');

  const img2 = new Image();
  img2.onload = function () {
    ctx2.drawImage(img2, 0, 0, canvasToFind.width, canvasToFind.height);
    const imageData = ctx2.getImageData(
      0,
      0,
      canvasToFind.width,
      canvasToFind.height
    );
    const data = imageData.data;

    userToFindInRgbaArray = [];
    for (let i = 0; i < data.length; i += 4) {
      const red = data[i];
      const green = data[i + 1];
      const blue = data[i + 2];
      const alpha = data[i + 3];
      userToFindInRgbaArray.push([red, green, blue, alpha]);
    }
    console.log(userToFindInRgbaArray);
  };
  img2.src = 'maria4.jpg';
};

async function findUser() {
  body = {
    image: userToFindInRgbaArray,
  };

  resp = await fetch('http://localhost:3000/face/find-user/', {
    headers: {
      accept: 'application/json',
      'accept-language': 'es-MX,es',
      'content-type': 'application/json',
    },
    body: JSON.stringify(body),
    method: 'POST',
  });
}

async function saveUserImage() {
  body = {
    photos: [
      {
        type: 'PROFILE',
        photo: userExampleInRgbaArray,
      },
      {
        type: 'SYSTEM',
        photo: userExampleInRgbaArray,
      },
    ],
  };

  resp = await fetch('http://localhost:3000/user/3/image/', {
    headers: {
      accept: 'application/json',
      'accept-language': 'es-MX,es',
      'content-type': 'application/json',
    },
    body: JSON.stringify(body),
    method: 'POST',
  });
}

async function save() {
  body = {
    name: 'iLabTDI',
    description: 'La mejor area de todas claro que si',
    module: 'N',
    classroom: '001',
    campus: 'CUCEI',
    department: 'Ingenierias',
    division: 'DIVEC',
    image: userExampleInRgbaArray,
  };

  resp = await fetch('http://localhost:3000/area/', {
    headers: {
      accept: 'application/json',
      'accept-language': 'es-MX,es',
      'content-type': 'application/json',
    },
    body: JSON.stringify(body),
    method: 'POST',
  });
}

async function getFromBack() {
  const response = await fetch('http://localhost:3000/area/4');
  const data = await response.json();
  const imageArray = data.image;
  const canvas = document.getElementById('fromWebCanvas');
  const ctx = canvas.getContext('2d');

  let x = 0;
  let y = 0;
  for (let pixel of imageArray) {
    const [r, g, b, a] = pixel;
    ctx.fillStyle = `rgba(${r}, ${g}, ${b}, ${a})`;
    ctx.fillRect(x, y, 1, 1);
    x++;
    if (x === canvas.width) {
      x = 0;
      y++;
    }
  }
}
