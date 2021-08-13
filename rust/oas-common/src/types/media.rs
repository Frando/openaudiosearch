use crate::mapping::Mappable;
use crate::record::TypedValue;
use crate::task::{TaskObject, TaskState};
use crate::ElasticMapping;
use schemars::JsonSchema;
use serde::{Deserialize, Serialize};
use serde_json::json;

use crate::ser;

#[derive(Serialize, Deserialize, Debug, Clone, Default, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct Media {
    pub content_url: String,
    pub encoding_format: Option<String>,
    #[serde(default)]
    #[serde(deserialize_with = "ser::deserialize_duration")]
    pub duration: Option<f32>,
    pub transcript: Option<Transcript>,
    pub nlp: Option<serde_json::Value>,

    #[serde(flatten)]
    pub other: serde_json::Map<String, serde_json::Value>,

    #[serde(default)]
    pub tasks: MediaTasks,
}

#[derive(Serialize, Deserialize, Debug, Clone, Default, JsonSchema)]
pub struct MediaTasks {
    pub download: Option<TaskState>,
    pub asr: Option<TaskState>,
}

impl TaskObject for Media {
    type TaskStates = MediaTasks;
    fn task_states(&self) -> Option<&Self::TaskStates> {
        Some(&self.tasks)
    }
    fn task_states_mut(&mut self) -> Option<&mut Self::TaskStates> {
        Some(&mut self.tasks)
    }
}

// pub struct MediaOpts {
//     pub wants_asr: bool,
//     pub wants_nlp: bool
// }

#[derive(Serialize, Deserialize, Debug, Clone, Default, JsonSchema)]
pub struct Transcript {
    pub text: String,
    pub parts: Vec<TranscriptPart>,
}

#[derive(Serialize, Deserialize, Debug, Clone, Default, JsonSchema)]
pub struct TranscriptPart {
    pub conf: f32,
    pub start: f32,
    pub end: f32,
    pub word: String,
}

impl TypedValue for Media {
    const NAME: &'static str = "oas.Media";
}

impl Mappable for Media {}

impl ElasticMapping for Media {
    fn elastic_mapping() -> Option<serde_json::Value> {
        Some(json!({
            "contentUrl":{
                "type":"text",
            },
            "duration": {
                "type": "float"
            },
            "encodingFormat": {
                "type": "keyword"
            },
            "nlp": {
                "type": "object"
            },
            "transcript": {
                "type": "object"
            }
        }))
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn deserialize_duration() {
        let source = r#"
        {
            "contentUrl": "foo",
            "duration": "02:03"
        }
        "#;

        let media: Media = serde_json::from_str(source).expect("failed to deserialize");
        assert_eq!(media.duration, Some(123.));

        let source = r#"
       {
           "contentUrl": "foo",
           "duration": "02:03:01"
       }
       "#;

        let media: Media = serde_json::from_str(source).expect("failed to deserialize");
        assert_eq!(media.duration, Some(7381.));

        let source = r#"
       {
           "contentUrl": "foo",
           "duration": "64"
       }
       "#;

        let media: Media = serde_json::from_str(source).expect("failed to deserialize");
        assert_eq!(media.duration, Some(64.));

        let source = r#"
        {
            "contentUrl": "foo",
            "duration": 123
        }
        "#;

        let media: Media = serde_json::from_str(source).expect("failed to deserialize");
        assert_eq!(media.duration, Some(123.));

        let source = r#"
        {
            "contentUrl": "foo",
            "duration": 562.5011
        }
        "#;

        let media: Media = serde_json::from_str(source).expect("failed to deserialize");
        assert_eq!(media.duration, Some(562.5011));

        let source = r#"
       {
           "contentUrl": "foo"
       }
       "#;

        let media: Media = serde_json::from_str(source).expect("failed to deserialize");
        assert_eq!(media.duration, None);
    }
}
