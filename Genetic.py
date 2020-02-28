{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "name": "Untitled3.ipynb",
      "provenance": [],
      "collapsed_sections": [],
      "authorship_tag": "ABX9TyOS/CpThbhQuZM0ry3z1evv",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/NRamjuttun1/Grammatical-Inference-Project/blob/master/Genetic.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "Zcwhb-kYKR--",
        "colab_type": "code",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 72
        },
        "outputId": "9a96572e-6d62-4fd9-f162-4694635f2d5e"
      },
      "source": [
        "from amnesiac import blurry_memory\n",
        "import random\n",
        "\n",
        "def getNewChar():\n",
        "  newstring = \"\"\n",
        "  newint = random.randint(65,101)\n",
        "  if (newint <= 90):\n",
        "      newstring += chr(newint)\n",
        "  elif (newint <= 100):\n",
        "    newstring += str((newint - 91))\n",
        "  elif (newint == 101):\n",
        "    newstring += \"_\"\n",
        "  return newstring\n",
        "\n",
        "def crossOver(pos1, pos2):\n",
        "  point = random.randint(1, 9)\n",
        "  bstr1 = samples[pos1][0:point]\n",
        "  estr1 = samples[pos1][point:]\n",
        "  bstr2 = samples[pos2][0:point]\n",
        "  estr2 = samples[pos2][point:]\n",
        "  samples[pos1] = bstr1 + estr2\n",
        "  samples[pos2] = bstr2 + estr1\n",
        "\n",
        "def mutation(pos):\n",
        "  samples[pos] = getNewChar()\n",
        "\n",
        "def checkFitnessForPass1(arr):\n",
        "  return blurry_memory(arr, 170180425, 0)\n",
        "\n",
        "def checkFitnessForPass2(arr):\n",
        "  return blurry_memory(arr, 170180425, 1)\n",
        "\n",
        "samplesize = 10\n",
        "samples = []\n",
        "for i in range(samplesize):\n",
        "  newstring = \"\"\n",
        "  for j in range(10):\n",
        "    newstring += getNewChar()\n",
        "  samples.append(newstring)\n",
        "print(samples)\n",
        "print(checkFitnessForPass1(samples))\n"
      ],
      "execution_count": 112,
      "outputs": [
        {
          "output_type": "stream",
          "text": [
            "['9MHL23_MYR', 'QD88UONZ63', '8ZL9R9IQTR', '9I9J6XU5Z0', '3WBMGPFM2B', 'ARQOUK3AUP', 'CVJSC0YM6F', 'U8L3ABM4VW', '43J0I5DDW6', 'RNLL_PJZR7']\n",
            "{'9MHL23_MYR': 0.4659266110644875, 'QD88UONZ63': 0.3697659892531798, '8ZL9R9IQTR': 0.5397163840567525, '9I9J6XU5Z0': 0.36692086700581406, '3WBMGPFM2B': 0.4624471426055978, 'ARQOUK3AUP': 0.536201191424917, 'CVJSC0YM6F': 0.49108043933205525, 'U8L3ABM4VW': 0.43396888263824307, '43J0I5DDW6': 0.48139283287470436, 'RNLL_PJZR7': 0.46036851522612054}\n"
          ],
          "name": "stdout"
        }
      ]
    }
  ]
}