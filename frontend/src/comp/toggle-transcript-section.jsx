import React from 'react'
import { Box, Text, Button, Flex } from '@chakra-ui/react'
import { FaChevronRight, FaChevronDown } from 'react-icons/fa'
import { useTranslation } from 'react-i18next'

export function ToggleTranscriptSection(props = {}) {
  const { post } = props
  const [show, setShow] = React.useState(false)
  const toggleTranscript = () => setShow(!show)
  if (!post) return null

  const transcript = post.media.map((media) => {
    if (media.transcript && media.transcript.text)
      return <Text>{media.transcript.text}</Text>
    return null
  })
  const { t } = useTranslation()
  console.log(transcript)

  return (
    <Box>
      {transcript.indexOf(null) < 0 &&
      <Box>
        <Button
          onClick={toggleTranscript}
          borderRadius='0'
        >
          <Flex direction="row"> 
            {show ? <Box mr='4px'><FaChevronDown /></Box> : <Box mr='4px'><FaChevronRight /></Box>}
            {show ? <Text>{t('transcript.hide', 'Hide transcript')}</Text> : <Text>{t('transcript.show', 'Show transcript')}</Text>}
          </Flex>
        </Button>
        {show &&
        <Box bg='gray.100' p='4'>
          {transcript}
        </Box>
        }
      </Box>
      }
    </Box>
  )
}
