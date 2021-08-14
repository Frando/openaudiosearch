import React from 'react'
import { DataSearch, ReactiveBase, ReactiveList } from '@appbaseio/reactivesearch'
import { Heading, Flex, Box, Spinner, Center, SimpleGrid } from '@chakra-ui/react'
import { API_ENDPOINT } from '../lib/config'
import { Link, useHistory } from 'react-router-dom'
import Moment from 'moment'
import { useTranslation } from 'react-i18next'
import { PostButtons } from './post'
import { ResultItem } from './search'

export default function LandingPage () {
  const url = API_ENDPOINT + '/search'
  const [value, setValue] = React.useState('')
  const history = useHistory()
  const { t } = useTranslation()
  return (
    <Center>
      <Flex color='white' align='center' justify='center'>
        <ReactiveBase
          app='oas'
          url={url}
        >
          <Flex direction='column' align='center'>
            <Flex direction='column' align='center'>
              <Heading as='h1' size='2xl' mt={[2, 2, 4, 4]}  mb='8' color='secondary.600'>{t('openaudiosearch', 'Open Audio Search')}</Heading>
              <Heading as='h2' size='lg' fontWeight='normal' mb='2'>{t('slogan', 'The community media search engine')}</Heading>
              <Center>
                <Box w={['90vw', '80vw', '600px', '600px']} mt='6'>
                  <DataSearch
                    componentId='searchbox'
                    dataField={['headline', 'description', 'transcript']}
                    fieldWeights={[5, 2, 1]}
                    placeholder={t('searchForm.placeholder', 'Search for community media')}
                    autosuggest
                    queryFormat='and'
                    fuzziness={0}
                    debounce={2000}
                    value={value}
                    onChange={(value, triggerQuery, event) => {
                      setValue(value)
                    }}
                    onValueSelected={(value, cause, source) => {
                      const encoded = encodeURIComponent(value)
                      history.push('/search/' + encoded)
                    }}
                  />
                </Box>
              </Center>
            </Flex>
            <Flex direction='column' align='left' maxWidth='750px'>
              <Box>
                <Heading as='h4' size='md' mt='20' mb='5' ml='5'>{t('discover', 'Discover')}</Heading>
              </Box>
              <ReactiveList
                dataField='datePublished'
                sortBy='desc'
                componentId='DiscoverItems'
                infiniteScroll={false}
                showResultStats={false}
                size={10}
                pagination={true}
                scrollOnChange={false}
              >
                {({ data, error, loading, ...args }) => {
                  if (loading) return <Spinner size='xl' />
                  return (
                    <SimpleGrid columns={[1, 1, 2, 2]} spacing={10}>
                      {
                        data.map((item, i) => (
                          <ResultItem item={item} key={i} showSnippets={false} />
                        ))
                      }
                    </SimpleGrid>
                  )
                }}
              </ReactiveList>
            </Flex>
          </Flex>
        </ReactiveBase>
      </Flex>
    </Center>
  )
}
